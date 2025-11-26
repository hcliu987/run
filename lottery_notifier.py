import requests
import os
import time
from datetime import datetime

class LotteryNotifier:
    def __init__(self, bark_key, numbers):
        self.bark_url = f"https://api.day.app/{bark_key}"
        # 验证并存储多组双色球号码
        self.numbers = []
        for number in numbers.strip().split('\n'):
            if number.strip():  # 忽略空行
                self.numbers.append(self._validate_numbers(number.strip()))

    def _validate_numbers(self, numbers):
        """验证双色球号码格式"""
        try:
            red, blue = numbers.split('+')
            red_numbers = [int(x) for x in red.split(',')]
            blue_number = int(blue)
            
            # 验证红球
            if len(red_numbers) != 6 or not all(1 <= x <= 33 for x in red_numbers):
                raise ValueError("红球必须是6个1-33之间的数字")
            
            # 验证蓝球
            if not 1 <= blue_number <= 16:
                raise ValueError("蓝球必须是1-16之间的数字")
                
            return {'red': red_numbers, 'blue': blue_number}
        except Exception as e:
            raise ValueError(f"号码格式错误: {str(e)}")

    def _check_prize(self, bet_numbers, result_numbers):
        """检查中奖情况"""
        bet_red = set(bet_numbers['red'])
        result_red = set(int(x) for x in result_numbers['红球'].split(','))
        red_matches = len(bet_red.intersection(result_red))
        blue_match = bet_numbers['blue'] == int(result_numbers['蓝球'])
        
        # 判断中奖等级及金额
        if red_matches == 6 and blue_match:
            return {"level": "一等奖", "amount": "浮动", "is_jackpot": True}
        elif red_matches == 6:
            return {"level": "二等奖", "amount": "浮动(约100万)", "is_jackpot": False}
        elif red_matches == 5 and blue_match:
            return {"level": "三等奖", "amount": "3000元", "is_jackpot": False}
        elif red_matches == 5 or (red_matches == 4 and blue_match):
            return {"level": "四等奖", "amount": "200元", "is_jackpot": False}
        elif red_matches == 4 or (red_matches == 3 and blue_match):
            return {"level": "五等奖", "amount": "10元", "is_jackpot": False}
        elif blue_match:
            return {"level": "六等奖", "amount": "5元", "is_jackpot": False}
        return {"level": "未中奖", "amount": "0元", "is_jackpot": False}

    def check_and_notify(self):
        result = self.get_lottery_result()
        if result:
            # 检查所有号码的中奖情况
            prize_results = []
            has_jackpot = False
            
            for idx, number in enumerate(self.numbers, 1):
                prize = self._check_prize(number, result)
                if prize["is_jackpot"]:
                    has_jackpot = True
                prize_results.append(
                    f"您的号码{idx}（{','.join(map(str, number['red']))}+{number['blue']}）：{prize['level']} {prize['amount']}"
                )
            
            title = f"双色球第{result['期号']}期开奖结果"
            if has_jackpot:
                title = f"🎉恭喜中得一等奖！- {title}"
            
            content = (
                f"开奖日期：{result['开奖日期']}\n"
                f"开奖号码：\n"
                f"红球：{result['红球']}\n"
                f"蓝球：{result['蓝球']}\n\n"
                f"{chr(10).join(prize_results)}"
            )
            self.send_notification(title, content)

    def get_lottery_result(self):
        """获取最新的双色球开奖结果"""
        try:
            url = "http://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issueCount=1"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if data["result"]:
                latest = data["result"][0]
                return {
                    "期号": latest["code"],
                    "开奖日期": latest["date"],
                    "红球": latest["red"],
                    "蓝球": latest["blue"]
                }
            return None
        except Exception as e:
            print(f"获取开奖结果失败: {str(e)}")
            return None

    def send_notification(self, title, content):
        """发送Bark通知"""
        try:
            response = requests.get(
                self.bark_url,
                params={
                    "title": title,
                    "body": content,
                    "group": "双色球开奖"
                }
            )
            if response.status_code == 200:
                print("通知发送成功")
                print(datetime.now())

            else:
                print(f"通知发送失败: {response.text}")
        except Exception as e:
            print(f"通知发送失败: {str(e)}")

def main():
    # 从环境变量获取配置，如果没有则使用默认值
    bark_key = os.getenv('BARK_KEY', 'qEnhyuDqQAcAtCKRCBWJ4e')
    
    # 默认的双色球号码列表
    default_numbers = """11,13,17,20,23,31+11
01,04,16,17,21,25+06"""
    
    numbers = os.getenv('LOTTERY_NUMBERS', default_numbers)  # 获取双色球号码列表
    
    notifier = LotteryNotifier(bark_key, numbers)
    notifier.check_and_notify()


if __name__ == "__main__":
    main()