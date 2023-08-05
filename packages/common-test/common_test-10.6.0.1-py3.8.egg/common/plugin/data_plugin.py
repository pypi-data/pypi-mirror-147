import json

from common.common.constant import Constant

from common.autotest.handle_allure import allure_title, allure_severity, allure_feature, allure_link, allure_story

from common.data.data_process import DataProcess

from common.data.handle_common import req_expr, convert_json, extractor
from common.plat.jira_platform import JiraPlatForm


class DataPlugin(object):
    @classmethod
    def convert_json(self, _temp, _replace: bool = True):
        """
        任意的数据类型转换成Json
        :param _temp:
        :param _replace: 是否清洗数据
        :return:
        """
        content = _temp
        if isinstance(_temp, str):
            content = json.loads(content)
        else:
            content = json.dumps(_temp)
        if _replace:
            content = req_expr(content)
        return content

    @classmethod
    def json_convert_dict(self, _json, _replace: bool = True) -> dict:
        """
              Json字符串转换为字典
              :param _json:
              :param _replace: 是否清洗数据
              :return:
              """
        if _replace:
            _json = req_expr(_json)
        return convert_json(_json)

    @classmethod
    def get_key_dic(self,_data, key):
        return DataProcess.get_key_dic(_data,key)


    @classmethod
    def get_json_by_jpath(self, obj: dict, expr: str = '.', error_flag: bool = False):
        """
            通过Jpath获取json数据
        :param obj:
        :param expr:
        :param error_flag:
        :return:
        """
        return extractor(obj, expr, error_flag)



    @classmethod
    def excel_convert_allure(self, data):
        if isinstance(data, dict):
            _title = DataProcess.get_key_dic(data,Constant.CASE_TITLE)
            _severity = DataProcess.get_key_dic(data,Constant.CASE_PRIORITY)
            _feature = DataProcess.get_key_dic(data,Constant.CASE_MODEL)
            _StoryName = DataProcess.get_key_dic(data,Constant.CASE_MODEL)
            _StoryLink = ""
            if DataProcess.get_key_dic(data, Constant.CASE_STORY_NO) is not None and str(
                    DataProcess.get_key_dic(data, Constant.CASE_STORY_NO)).strip() != '':
                _StoryName, _StoryLink = JiraPlatForm.getJiraIssueSummer(DataProcess.get_key_dic(data, Constant.CASE_STORY_NO))
            if DataProcess.get_key_dic(data,Constant.CASE_LINK) is not None and str(
                    DataProcess.get_key_dic(data, Constant.CASE_LINK)).strip() != '':
                _StoryName, _StoryLink = JiraPlatForm.getJiraIssueSummer(DataProcess.get_key_dic(data,Constant.CASE_LINK))
            if _StoryName is None:
                _StoryName = str(DataProcess.get_key_dic(data, Constant.CASE_STORY)).strip()
                _StoryLink = str(DataProcess.get_key_dic(data, Constant.CASE_LINK)).strip()
        if isinstance(data, list):
            _feature = data[1]
            _StoryName, _StoryLink = JiraPlatForm.getJiraIssueSummer(
                data[2].strip())
            if _StoryName is not None:
                _title = data[3]
                _severity = data[4]
            else:
                _StoryName, _StoryLink = JiraPlatForm.getJiraIssueSummer(
                    data[3].strip())
                if _StoryName is not None:
                    _title = data[4]
                    _severity = data[5]
                else:
                    _StoryName = data[2]
                    _StoryLink = data[3]
                    _title = data[4]
                    _severity = data[5]

        allure_title(_title)
        # allure报告 用例模块
        allure_feature(_feature)
        # allure报告用例优先级
        allure_severity(_severity)
        allure_story(_StoryName)
        allure_link(_StoryLink)






if __name__ == '__main__':
    str1 = '{"listData": "333","strData": "test python obj 2 json"}'
    print(DataPlugin.convert_json(str1))





