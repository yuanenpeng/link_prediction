import os
import io
import re
from collections import defaultdict


def read_singlepaper(file):
    paper_info = {}
    author_info = {}
    s = file.readlines()
    sectionMark = '\\\\\n'
    count_sectionMark = 0

    for index, item in enumerate(s):
        if 'Paper' in item:
            paper_id = item.split('/')[-1].strip()
            break
    print(paper_id)
    paper_info[paper_id] = {}  # construct a sub dictionary, paper_id is key
    for index, item in enumerate(s):
        if 'Author' in item:
            item = re.sub("[\(\[].*?[\)\]]", "", item)
            if 'department' in item.lower():
                item = item.replace('Department', '')
            if 'university' in item.lower():
                item = item.replace('University', '')
            if 'and' in item:
                item = item.replace('and', ',')
            author_list = item.split(':')[-1]
            author_list = author_list.split(',')
            author_list = [j.strip() for j in author_list]
            try:
                author_list.remove('')
            except:
                pass
            paper_info[paper_id]['author_list'] = author_list

            # author dictionary
            for j in author_list:
                author_info[j] = paper_id

        if item == sectionMark:
            count_sectionMark += 1
        if count_sectionMark == 2:
            abstracts = s[index+1:-1]
            abstracts = [j.strip() for j in abstracts]
            abstracts = ' '.join(abstracts)
            paper_info[paper_id]['abstracts'] = abstracts
            # paper_info['abstracts'] = abstracts
            break
    return paper_info, author_info


def main():
    path = os.getcwd() + '/data_PGM/hep-th-abs.tar/'
    paper_info_allFolder = {}
    author_info_allFolder = defaultdict(list)
    for subdir, dirs, files in os.walk(path):
        if dirs == []:  # so we skip the parent directory
            for filename in os.listdir(subdir):
                f = io.open(subdir + '/' + filename)
                paper_info, author_info = read_singlepaper(f)
                paper_info_allFolder.update(paper_info)
                # 'update' will overwrite, but paper_info has unique keys, so okay here
                for key, value in author_info.items():
                    author_info_allFolder[key].append(value)
    print(author_info_allFolder)


# test for appending values to same key
# d1 = {1: 2, 3: 4, 5: 6}
# d2 = {1: 6, 3: 7}
# d3 = {1: 5, 3: 8}
# dd = defaultdict(list)
#
# for d in (d1, d2, d3): # you can list as many input dicts as you want here
#     for key, value in d.items():
#         dd[key].append(value)
# print(dd)
# or in our case, we can do:
# for key, value in d1.items():
#     dd[key].append(value)
# for key, value in d2.items():
#     dd[key].append(value)
# for key, value in d3.items():
#     dd[key].append(value)
# print(dd)


if __name__ == '__main__':
    main()




