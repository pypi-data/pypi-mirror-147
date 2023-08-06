import time
from faker import Faker


class MockData:
    def __init__(self, locale=None):
        """
        指定语言
        @param locale: 默认中文zh_CN，英文en_US
        """
        if locale is not None:
            self.fake = Faker(locale)
        else:
            self.fake = Faker()

    @property
    def now_time(self):
        """
        当前时间
        @return: 年-月-日 时-分-秒
        """
        return time.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def timestamp(n=10):
        """
        当前时间戳，10位是秒，13位是毫秒
        @param n: 指定时间戳的位数，不够位数右边补充6
        @return: 时间戳
        """
        _timestamp = (str(time.time()).replace('.', '')[:n]).ljust(n, '6')
        return _timestamp

    @property
    def date(self):
        """
        当前日期
        @return: 年-月-日
        """
        return self.fake.date(pattern="%Y-%m-%d")

    @property
    def timezone(self):
        """时区"""
        return self.fake.timezone()

    @property
    def name(self):
        """
        姓名
        @return: 设置的locale不同，返回的语言文本不同
        """
        return self.fake.name()

    @property
    def company(self):
        """
        公司名
        @return:
        """
        return self.fake.company()

    @property
    def address(self):
        """
        地址
        @return:
        """
        return self.fake.address()

    @property
    def province(self):
        """
        省
        @return:
        """
        return self.fake.province()

    @property
    def city(self):
        """
        市
        @return:
        """
        return self.fake.city()

    @property
    def county(self):
        """
        区
        @return:
        """
        return self.fake.district()

    @property
    def street(self):
        """
        街道
        @return:
        """
        return self.fake.street_address()

    @property
    def phone_number(self):
        # """
        # 根据时间戳生成一个不重复的手机号
        # @return: 13652435335
        # """
        # # 移动手机号前几位
        # cm = [134, 135, 136, 137, 138, 139, 150, 151, 152, 157, 158, 159, 182, 183, 184, 187, 188, 147, 178, 1705]
        # # 联通手机号前几位
        # cu = [130, 131, 132, 155, 156, 185, 186, 145, 176, 1709]
        # # 手机号前几位
        # ct = [133, 153, 180, 181, 189, 177, 1700]
        # phone = str(random.choice(cm + cu + ct)) + MockData.timestamp(7)
        # phone = phone[:11]
        return self.fake.phone_number()

    @property
    def credit_card_number(self):
        """
        信用卡号码
        @return:
        """
        return self.fake.credit_card_number()

    @property
    def email(self):
        """邮箱"""
        return self.fake.email()

    @property
    def ssn(self):
        """身份证"""
        return self.fake.ssn()

    @property
    def word(self):
        """关键词"""
        return self.fake.word()

    def words(self, n):
        """关键词列表"""
        return self.fake.words(nb=n)


if __name__ == '__main__':
    mock_cn = MockData('zh_CN')
    mock_en = MockData()
    print(mock_cn.now_time)
    print(mock_cn.date)
    print(mock_cn.timestamp())
    print(mock_cn.timezone)
    print(mock_cn.name)
    print(mock_en.name)
    print(mock_cn.company)
    print(mock_cn.address)
    print(mock_en.address)
    print(mock_cn.province)
    print(mock_cn.city)
    print(mock_cn.county)
    print(mock_cn.credit_card_number)
    print(mock_cn.phone_number)
    print(mock_cn.email)
    print(mock_cn.ssn)
    print(mock_cn.word)
    print(mock_cn.words(3))









