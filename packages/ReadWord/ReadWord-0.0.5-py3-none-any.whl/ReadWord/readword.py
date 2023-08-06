import shutil
import time
from bs4 import BeautifulSoup
from pathlib import Path
import zipfile
from functools import lru_cache


class RW:
    def __init__(self, filepath):
        self.__filepath = filepath
        self.__pj_path = Path(__file__).resolve().parent / 'TempFolder'

    def create_workspace(self):
        if self.__pj_path.exists():
            shutil.rmtree(self.__pj_path)
            self.__pj_path.mkdir(parents=True, exist_ok=True)
        else:
            self.__pj_path.mkdir(parents=True, exist_ok=True)
        temp_path = shutil.copy(self.__filepath, self.__pj_path)
        temp_path = Path(temp_path).replace(Path(temp_path).with_suffix('.zip'))
        zip_file = zipfile.ZipFile(temp_path)
        zip_file.extractall(self.__pj_path)

    def save_all_picture(self, path):
        try:
            pics = self.__pj_path / 'word' / 'media'
            wait_time = 1
            while True:
                if pics.exists():
                    all_pic = pics.glob('*png')
                    for i in all_pic:
                        shutil.copy(i, path)
                    break
                elif wait_time == 4:
                    raise Exception("No workspace found !!!")
                else:
                    time.sleep(0.5)
                    wait_time += 1
        except Exception as e:
            print(e)

    @lru_cache()
    def get_style_position(self):
        try:
            document_file = self.__pj_path/'word'/'document.xml'
            wait_time = 1
            all_content = []
            while True:
                if document_file.exists():
                    with open(document_file, 'r', encoding='utf8') as f:
                        source = f.read()
                        soup = BeautifulSoup(source, 'xml')
                        paragraphs = soup.find('w:body').children
                        # print(paragraphs)
                        for paragraph in paragraphs:
                            str_paragraphs = str(paragraph)
                            if str_paragraphs.startswith('<w:p'):
                                if 'w:val=' in str_paragraphs:
                                    if 'w:val="1"' in str_paragraphs:
                                        all_content.append({"heading 1": paragraph.text})
                                    elif 'w:val="2"' in str_paragraphs:
                                        all_content.append({"heading 2": paragraph.text})
                                    elif 'w:val="3"' in str_paragraphs:
                                        all_content.append({"heading 3": paragraph.text})
                                    elif 'w:val="4"' in str_paragraphs:
                                        all_content.append({"heading 4": paragraph.text})
                                    else:
                                        all_content.append({"otherheading": paragraph.text})
                                elif 'wp:docPr' in str_paragraphs:
                                    picname = paragraph.find('wp:docPr').get("name")
                                    all_content.append({"picture": picname})
                                elif ('w:pStyle' and 'w:drawing') not in str_paragraphs:
                                    all_content.append({"normal": paragraph.text})
                            elif str_paragraphs.startswith('<w:tbl'):
                                # value_count = len(paragraph.find('w:tblGrid').find_all('w:gridCol'))
                                values = paragraph.find_all('w:tr')
                                valueslist = []
                                for tr in values:
                                    tr_values = tr.find_all("w:tc")
                                    tc = [x.text for x in tr_values]
                                    valueslist.append(tc)
                                all_content.append({"table": valueslist})
                        return all_content
                elif wait_time == 4:
                    raise Exception("No document file found !!!")
                else:
                    time.sleep(0.5)
                    wait_time += 1
        except Exception as e:
            print(e)

    def exit(self):
        shutil.rmtree(self.__pj_path)
