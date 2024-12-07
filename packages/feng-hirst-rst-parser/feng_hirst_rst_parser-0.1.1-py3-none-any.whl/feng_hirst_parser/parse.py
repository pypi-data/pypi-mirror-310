'''
Created on 2014-01-17

@author: Vanessa Wei Feng
'''
from feng_hirst_parser.utils import serialize
from feng_hirst_parser.segmenters.crf_segmenter import CRFSegmenter
from feng_hirst_parser.treebuilder.build_tree_CRF import CRFTreeBuilder

from optparse import OptionParser
from copy import deepcopy
from feng_hirst_parser.utils import paths
import os.path
import re
import sys
from feng_hirst_parser.document.doc import Document
import time
import traceback
from datetime import datetime

from feng_hirst_parser.logs.log_writer import LogWriter
from feng_hirst_parser.prep.preprocesser import Preprocesser

PARA_END_RE = re.compile(r' (<P>|<s>)$')
v = '2.0'


class DiscourseParser:
    def __init__(
            self,
            verbose: bool,
            skip_parsing: bool,
            global_features: bool,
            save_preprocessed_doc: bool,
            output_dir: str,
            log_writer=None
    ):
        """
        Initialize the parser.
        :param verbose: Activates verbose mode.
        :param skip_parsing: Skip parsing, i.e., conduct segmentation only.
        :param global_features: Perform a second pass of EDU segmentation using global features.
        :param save_preprocessed_doc: Save preprocessed document into serialized file for future use.
        :param output_dir: Specify a directory for output files.
        :param log_writer: Perform logging while parsing.
        """
        self.verbose = verbose
        self.skip_parsing = skip_parsing
        self.global_features = global_features
        self.save_preprocessed_doc = save_preprocessed_doc

        self.output_dir = os.path.join(output_dir)
        self.log_writer = LogWriter(log_writer)
        self.feature_sets = 'gCRF'

        init_start = time.time()

        self.preprocesser = None
        try:
            self.preprocesser = Preprocesser()
        except Exception as e:
            print("*** Loading Preprocessing module failed...")
            print(traceback.print_exc())

            raise e
        try:
            self.segmenter = CRFSegmenter(
                _name=self.feature_sets,
                verbose=self.verbose,
                global_features=self.global_features
            )
        except Exception as e:
            print("*** Loading Segmentation module failed...")
            print(traceback.print_exc())
            raise e

        try:
            if not self.skip_parsing:
                self.treebuilder = CRFTreeBuilder(_name=self.feature_sets, verbose=self.verbose)
            else:
                self.treebuilder = None
        except Exception as e:
            print("*** Loading Tree-building module failed...")
            print(traceback.print_exc())
            raise e

        init_end = time.time()
        print(f'Finished initialization in {init_end - init_start:.2f} %.2f seconds.\n')

    def unload(self):
        if self.preprocesser is not None:
            self.preprocesser.unload()

        if self.segmenter is not None:
            self.segmenter.unload()

        if self.treebuilder is not None:
            self.treebuilder.unload()

    def parse_from_text(
            self,
            text: str,
            identifier: str
    ):
        try:
            import spacy
        except ImportError:
            raise ImportError('Please install spacy to use this function.\nDownload the following model as well: python -m spacy download en_core_web_sm')
        serialized_doc_filename = os.path.join(self.output_dir, identifier + '.doc.ser')
        doc = None
        if os.path.exists(serialized_doc_filename):
            doc = serialize.load_data(identifier, self.output_dir, '.doc.ser')
        if doc is None or not doc.preprocessed:
            preprocess_start = time.time()
            doc = Document()
            doc.preprocess_from_text(text, self.preprocesser)
            preprocess_end = time.time()
            msg = f'Finished preprocessing in {preprocess_end - preprocess_start:.2f} seconds.'
            print(msg)
            self.log_writer.write(msg)
            if self.save_preprocessed_doc:
                print(f'Saved preprocessed document data to {serialized_doc_filename}.')
                serialize.save_data(identifier, doc, self.output_dir, '.doc.ser')
        else:
            print('Loaded saved serialized document data.')
        return self.process_parsed_doc(doc, identifier, serialized_doc_filename)

    def parse(self, filename):
        if not os.path.exists(filename):
            print(f'{filename} does not exist.')
            return

        self.log_writer.write(f'***** Parsing {filename}...')

        try:
            core_filename = os.path.split(filename)[1]
            serialized_doc_filename = os.path.join(self.output_dir, core_filename + '.doc.ser')
            doc = None
            if os.path.exists(serialized_doc_filename):
                doc = serialize.load_data(core_filename, self.output_dir, '.doc.ser')

            if doc is None or not doc.preprocessed:
                preprocess_start = time.time()
                doc = Document()
                doc.preprocess(filename, self.preprocesser)
                preprocess_end = time.time()
                msg = f'Finished preprocessing in {preprocess_end - preprocess_start:.2f} seconds.'
                print(msg)
                self.log_writer.write(msg)
                if self.save_preprocessed_doc:
                    print(f'Saved preprocessed document data to {serialized_doc_filename}.')
                    serialize.save_data(core_filename, doc, self.output_dir, '.doc.ser')
            else:
                print('Loaded saved serialized document data.')
            print('')
        except Exception as e:
            print("*** Preprocessing failed ***")
            print(traceback.print_exc())
            raise e

        return self.process_parsed_doc(doc, core_filename, serialized_doc_filename)

    def process_parsed_doc(self, doc, core_filename, serialized_doc_filename):
        result = None
        try:
            if not doc.segmented:
                seg_start = time.time()
                self.segmenter.segment(doc)

                if self.verbose:
                    print('edus')
                    for e in doc.edus:
                        print(e)
                    print(' ')
                    print('cuts')
                    for cut in doc.cuts:
                        print(cut)
                    print(' ')
                    print('edu_word_segmentation')

                seg_end = time.time()
                print(f'Finished segmentation in {seg_end - seg_start:.2f} seconds.')
                print(f'Segmented into {len(doc.edus)} EDUs.')

                self.log_writer.write(
                    f'Finished segmentation in {seg_end - seg_start:.2f} seconds. Segmented into {len(doc.edus)} EDUs.')
                if self.save_preprocessed_doc:
                    print(f'Saved segmented document data to {serialized_doc_filename}.')
                    serialize.save_data(core_filename, doc, self.output_dir, '.doc.ser')
            else:
                print(f'Already segmented into {len(doc.edus)} EDUs.')
            print(' ')

            if self.verbose:
                for e in doc.edus:
                    print(e)
        except Exception as e:
            print("*** Segmentation failed ***")
            print(traceback.print_exc())
            raise e

        try:
            ''' Step 2: build text-level discourse tree '''
            if self.skip_parsing:
                outfname = os.path.join(self.output_dir, core_filename + ".edus")
                print(f'Output EDU segmentation result to {outfname}')
                with open(outfname, 'w') as f_o:
                    for sentence in doc.sentences:
                        sent_id = sentence.sent_id
                        edu_segmentation = doc.edu_word_segmentation[sent_id]
                        i = 0
                        sent_out = []
                        for (j, token) in enumerate(sentence.tokens):
                            sent_out.append(token.word)
                            if j < len(sentence.tokens) - 1 and j == edu_segmentation[i][1] - 1:
                                sent_out.append('EDU_BREAK')
                                i += 1
                        f_o.write(' '.join(sent_out) + '\n')
            else:
                tree_build_start = time.time()
                outfname = os.path.join(self.output_dir, core_filename + ".tree")
                pt = self.treebuilder.build_tree(doc)
                print('Finished tree building.')
                if pt is None:
                    print("No tree could be built...")
                    if self.treebuilder is not None:
                        self.treebuilder.unload()
                    return -1
                # Unescape the parse tree
                if pt:
                    doc.discourse_tree = pt
                    result = deepcopy(pt)
                    tree_build_end = time.time()

                    msg = f'Finished tree building in {tree_build_end - tree_build_start:.2f}'
                    print(msg)
                    self.log_writer.write(msg)

                    for i in range(len(doc.edus)):
                        edu_str = ' '.join(doc.edus[i])
                        leaf_position = pt.leaf_treeposition(i)
                        pt[leaf_position] = f'!{edu_str}!'  # parse tree with escape symbols
                        result[leaf_position] = PARA_END_RE.sub('', edu_str)  # parse tree without escape symbols

                    out = pt.pformat()
                    print(f'Output tree building result to {outfname}.')
                    with open(outfname, 'w') as f_o:
                        f_o.write(out)
                if self.save_preprocessed_doc:
                    print(f'Saved fully processed document data to {serialized_doc_filename}.')
                    serialize.save_data(core_filename, doc, self.output_dir, '.doc.ser')
            print(' ')
        except Exception as e:
            print(traceback.print_exc())
            raise e
        print('===================================================')
        return result


def main(options, args):
    parser = None
    results = []

    try:
        if options.output_dir:
            output_dir = args[0]
            start_arg = 1
        else:
            output_dir = None
            start_arg = 0

        log_writer = None
        if options.logging:
            log_fname = os.path.join(paths.LOGS_PATH, 'log_%s.txt' % (
                output_dir if output_dir else datetime.now().strftime('%Y_%m_%d_%H_%M_%S')))
            log_writer = open(log_fname, 'w')

        if options.filelist:
            file_fname = args[start_arg]
            if not os.path.exists(file_fname) or not os.path.isfile(file_fname):
                print('The specified file list %s is not a file or does not exist' % file_fname)
                return

        parser = DiscourseParser(
            verbose=options.verbose,
            skip_parsing=options.skip_parsing,
            global_features=options.global_features,
            save_preprocessed_doc=options.save_preprocessed,
            output_dir=output_dir,
            log_writer=log_writer
        )

        files = []
        skips = 0
        if options.filelist:
            file_fname = args[start_arg]
            for line in open(file_fname).readlines():
                fname = line.strip()

                if os.path.exists(fname):
                    if os.path.exists(os.path.join(parser.output_dir, os.path.split(fname)[1] + '.tree')):
                        skips += 1
                    else:
                        files.append(fname)
                else:
                    skips += 1
        #                    print 'Skip %s since it does not exist.' % fname
        else:
            fname = args[start_arg]
            #            print os.path.join(paths.tmp_folder, os.path.split(fname)[1] + '.xml')
            if os.path.exists(fname):
                if os.path.exists(os.path.join(parser.output_dir, os.path.split(fname)[1] + '.tree')):
                    skips += 1
                else:
                    files.append(fname)
            else:
                skips += 1

        print('Processing %d documents, skipping %d' % (len(files), skips))

        for (i, filename) in enumerate(files):
            print('Parsing %s, progress: %.2f (%d out of %d)' % (filename, i * 100.0 / len(files), i, len(files)))

            try:
                result = parser.parse(filename)
                results.append(result)

                parser.log_writer.write('===================================================')
            except Exception as e:
                print('Some error occurred, skipping the file')
                raise e

        parser.unload()
        return results

    except Exception as e:
        if not parser is None:
            parser.unload()

        raise Exception(traceback.print_exc())


def parse_args():
    usage = "Usage: %prog [options] input_file/dir"

    optParser = OptionParser(usage=usage, version="%prog " + v)
    optParser.add_option("-v", "--verbose",
                         action="store_true", dest="verbose", default=False,
                         help="verbose mode")
    optParser.add_option("-s", "--skip_parsing",
                         action="store_true", dest="skip_parsing", default=False,
                         help="Skip parsing, i.e., conduct segmentation only.")
    optParser.add_option("-D", "--filelist",
                         action="store_true", dest="filelist", default=False,
                         help="parse all files specified in the filelist file, one file per line.")
    optParser.add_option("-t", "--output_dir",
                         action="store_true", dest="output_dir", default=False,
                         help="Specify a directory for output files.")
    optParser.add_option("-g", "--global_features",
                         action="store_true", dest="global_features", default=False,
                         help="Perform a second pass of EDU segmentation using global features.")
    optParser.add_option("-l", "--logging",
                         action="store_true", dest="logging", default=False,
                         help="Perform logging while parsing.")
    optParser.add_option("-e", "--save",
                         action="store_true", dest="save_preprocessed_doc", default=False,
                         help="Save preprocessed document into serialized file for future use.")

    (options, args) = optParser.parse_args()
    if len(args) == 0:
        optParser.print_help()
        sys.exit(1)

    return options, args


if __name__ == '__main__':
    options, args = parse_args()
    main(options, args)
