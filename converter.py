import glob
import os

import pandas as pd
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str,
                help="path to folder with ann and txt files")
args = vars(ap.parse_args())


class ConverterTsv(object):

    def __init__(self, workdir):
        self.workdir = workdir
        self.masks = []  # lists of processed annotations
        self.relations = []  # relations b/masks
        self.result_T = []
        self.result = []
        print(self.workdir, 'working folder')

    @staticmethod
    def sort_by_filename(val):
        if val.endswith('.ann'):

            return os.path.basename(val).split('.ann')[0]
        elif val.endswith('.txt'):
            return os.path.basename(val).split('.txt')[0]

    def create_paths(self):
        ann_paths = glob.glob(self.workdir + '/*.ann')
        txt_paths = glob.glob(self.workdir + '/*.txt')
        ann_paths.sort(key=self.sort_by_filename)
        txt_paths.sort(key=self.sort_by_filename)

        if len(ann_paths) != len(txt_paths):
            raise ValueError('Error oi ann or txt files numbers')

        # return ann_paths, txt_paths
        self.ann_paths = ann_paths
        self.txt_paths = txt_paths

    def create_lists(self):
        # create two lists from annotations: one for masks, one for relations between masks
        for i, path in enumerate(self.ann_paths):
            # print(path, self.txt_paths[i])

            ann_df = pd.read_csv(path, header=None, sep='\t')
            relation_list = [[ind, label.split(' '), pharase] for ind, label, pharase in
                             zip(ann_df[0], ann_df[1], ann_df[2]) if ind.startswith('R')]
            ann_list = [[ind, label.split(' '), pharase] for ind, label, pharase in zip(ann_df[0], ann_df[1], ann_df[2])
                        if ind.startswith('T')]
            ann_list.sort(key=self.sortSecond)

            self.masks.append(ann_list)
            self.relations.append(relation_list)

    @staticmethod
    def sortSecond(val):
        return int(val[1][1])

    @staticmethod
    def get_T(re_info):
        return re_info[1][1].split(':')[1], re_info[1][2].split(':')[1]

    @staticmethod
    def check_T(t_elem):
        # try -2
        if t_elem[-2:][0] == 'T':
            return t_elem[-2:]
        else:
            return t_elem[-3:]

    def embeding_T(self, a):
        res = []
        for i in a.split('@'):
            res.append(self.check_T(i))

        return res

    def check_relation(self, a, rel_list):
        for re_info in rel_list:
            if self.get_T(re_info)[0] and self.get_T(re_info)[1] in a:
                return '1'

    def add_masks_to_txt(self, txt_file, mask_list, add_T=True):
        with open(txt_file) as f:
            data = f.read().replace('\n', ' ')
            last_index = 0
            result = ''

            for ann_info in mask_list:
                crop = data[last_index:int(ann_info[1][2])]
                if add_T:
                    crop = crop.replace(ann_info[2], ann_info[0] + '@' + ann_info[1][0].upper() + '$', 1)
                else:
                    crop = crop.replace(ann_info[2], '@' + ann_info[1][0].upper() + '$', 1)

                last_index = int(ann_info[1][2])
                result += crop
            # print( len(result))
            if add_T:
                self.result_T.append(result)
            else:
                self.result.append(result)

    def create_dataset(self):
        for i, path in enumerate(self.txt_paths):
            # print(path)
            self.add_masks_to_txt(path, self.masks[i])
            self.add_masks_to_txt(path, self.masks[i], add_T=False)
            sentences_list = self.result_T[i].split('. ')  # split to sentences
            s_df = pd.DataFrame(sentences_list)  # to dataframe
            s_df['embeded'] = s_df[0].map(self.embeding_T)  # new column for splittetd on @ symbol
            s_df['relation'] = s_df['embeded'].apply(self.check_relation, args=(self.relations[i],))
            s_df[0] = self.result[i].split('. ')  # replace initial texts, so it contain masks without T-tags
            res = s_df[[0, 'relation']]
            tsv_name = path.replace('.txt', '.tsv')
            res.to_csv(tsv_name, sep='\t', na_rep='0', header=None, index=None)
workdir = args['input']
my_conv = ConverterTsv(workdir)
my_conv.create_paths()
my_conv.create_lists()
my_conv.create_dataset()
print('tsv created successfully in folder: {}'.format(workdir))
