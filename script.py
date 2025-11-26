# !/usr/bin/python3
# -- coding: utf-8 --
"""
打开小程序或APP-我的-积分, 捉以下几种url之一,把整个url放到变量 sfsyUrl 里,多账号换行分割
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/weChat/shareGiftReceiveRedirect
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect
每天跑一到两次就行
"""
# cron: 11 6,9,12,15,18 * * *
# const $ = new Env("顺丰速运");
import hashlib
import json
import os
import random
import time
import re
from datetime import datetime, timedelta
from sys import exit
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning

os.environ[
    "sfsyUrl"
] = """https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=yFI7g0PshvJkywfGn1RJ2PAkaY9TDxUV8urqTj%2B70bM03Mci%2FnUc9d3qNWSyWM%2BWzvg7o3%2FnnPf8LDs4k6%2BdHGCjGBgu6bZdZxURCCYaJfdzVCosFHH9sozLLSyoe%2FnA9G6%2Fj6T6zJoe9umQu%2BDYXoxy2HtL4z0R6UcvCaiZqLhSNAIIZgCEINvg3%2F%2BGeCqi5EOCl%2Fq22q0bfVdKvASWaVC3LLkVYXzcBlZU%2Bom3KWopriZFGbRu0DyC5x5x4f%2B12Fl66gVp%2Fjgpl1EYVCd9%2FFlH6Bbrrc5bspVhdQee6PWb6rCQYzt0yK%2BxHOiPmJj29uZagoCh6%2B9yP2gjCKUc%2Bg%3D%3D&source=SFAPP&bizCode=619
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=Ssggt0xeTcxtebBqCT2lo6eZqoPiUhliHFzT2EQGK4c2Rsnu8I1QBZOUFgVvLBo25rv7L1OPHLexZ0r0GAkhL8UDzbqteu9PwpjTkOy1TQbgjTS4c8W9qun%2FG3NSvRjlK7Te1L3qYhiP3mwzOprLYOYyhlGnYfsqUAx94YCvmsWLE5Vkt0xLdpdAjhi0sYVW0Bpx%2BRcUzIfghyYg0UQZP4%2F7YFT%2FWd0UhCNW9FESa1fU7l2pzf3vYP2JXL3Y%2B%2FhGL5ckiOOMfJaRtrfD%2Bm6W61HmA3Hn3zuiMLnmlTltjALnE0zy3Msp1WRSkk0IYLp%2Bnc8mWuHVykwMf3Om77ntUg%3D%3D&source=SFAPP&bizCode=619
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=XHBSVIobKfRz6diTi480%2BpVyLHOaCRdmjRiQZ2soOlPfKjkLz7SZAOYOgOEjwZOQZLkS8T0jqTKFXIiY27%2FKIOWNZyU0pXy7REivKPc7G%2BXm5yO32uTSQP3fRLmQDYXAGSV1eqiF1pGQRicNJq5m7TYkYmuXs8pzbUgD78NjemvuEnxnkzlXPimGfKyCbVvsiTlrlXPnGfdFc4UQ%2B5JDua2cgsgYjWzxotO2ar54MTTGVo2jiK3AXmiuxE2t1j5Glxf742jJb63RIfUO4rbD20gkwbXVAOH9bEDfbtw9DkT0M3Vin8St7gOwXEWPc0zrykq2%2Fy%2BajreZrPN9xnEriw%3D%3D&source=SFAPP&bizCode=619
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=MfZUJU9ZPmHdEFCHiinFUiFR97Q2TX4X%2FoIGKhfMYbH3vlFALjrjYFA8vxbKW7FCkeqZU%2FKcb5vJiampRzC7cGFmkM7MtJ00xQCIBBiAGkJYTMTnDaOFqlzuszCshP9VQJ1gGQ3QQRLXnmG5Xn2NTGUcwHIVVqaWG%2FjykYsOb%2B7vLfMKsnlWOZ9Yvjy6LYeXzPcgia9nBkX1bWxXC45tsC8PKxATFajwJ1H9%2BUDzjiuJqeO6bbyyJALz2yf201lG3yMS20qlCRyRbVtY9iXTDHgYMKFJOz8Cc7AvGmwPj8WHaVG27PdvmZI%2Ffu%2F%2B1ey%2BSMoOHGKT2m%2FmB6ZqKD8Siw%3D%3D&source=SFAPP&bizCode=619
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=YVE2czu03bRXiHbqAIew2pYrrSmx96h4SIFCnyubBzCk0qq1a9JRaDgtyQlzl3JdBrmrEUOX0TTZrtasOpv83LKnuJy4iGJQ%2B4VyxTbHzhJsMcp0HQYPxdjGeD1KprmzxQT0%2BbvkRZ36TfnHazAZe2AaSaifCP0xqmXr4%2Bk4o14QSbC0xr27bi29BU8Pldexunbv4MeN7Ak6%2BY7pdtKFD6jLbc8QAVEG7Sz7suIfZsxQGO4fJ0M2r9a6aYUlEuZj646gT05nmhXKkEh8NbJ81xfoJ03GLlSsEuc2NkRIQHrig8hNfHSwuRwngbw8tsLQmKalayQxc%2FQJMVHou%2FFVpA%3D%3D&source=SFAPP&bizCode=619
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=P5Tn%2Fye30Jrhz%2F1tWpguobXRxNc4VlkD5EDmyBq45Vw8GO3EXLRJSJp7fcDPI2ZUYEhQXyQ2r%2F92sgFpM9DWtKLCoXv%2BgLlZ3UGzWp1lX28zZImfgBe97hPbvWm0evtA%2BxhCRUqbaslamFdphhlFQBps1KUCdWuFc7ru9fiYuD9iqvmLjF483iEz7M4M0rR7JIk8Vev8yHPEPD0oeKFggPsv01RJl9GrnGm5MSWUjgq4Q1KWax8ljEQbrtxHSIKj7naL053cJBxj%2B%2BMlRbTlXmt2cU2KVr6Anwkqfhtc2Joh7zLymtYxz8sP8eBhvENJICSIkfhUItO3e7fSdMfuJg%3D%3D&source=SFAPP&bizCode=619
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=MWOX3rt4w6wAfj%2BnWmWjpyXN7dE0opGfRNRFWliActVntjyd2Mdqlbn1i6G7k6B3w2TKCvPWfPuoN4V7yFujy%2B7iqLHAMdMyB3GbwgBaVzKSbveD%2Bbyh6OYY1iSNRbSB9Hmvm890VCu5kyWIX6%2FPYgWXh5IGQc746BC3YKDyidmuO2RRIHSGhPSVXFp1NVrMh8C3BUt%2B6S7waL%2B0RMKuG5HSHaAjEbWwffRxpoiO1AMVlq6iFU53ef78R%2F1K15gykOnlwwRbV8VWIxRzJYZcX5bM9zNN9fOYi40h06xDZ1uQ9M6tadNg3BjnLF0N%2FZFGy%2BXp9Om2mcYhpYIRga9qTQ%3D%3D&source=SFAPP&bizCode=619
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=h7%2FnPZpiUf1VctIzErSkoSrcmqlXZ8KGXIVBUsOw6SDfUdsCn9ci8RCGvkkbO6VZwvQ4GcsKvVnfX4DtsV%2FLtcNfHUjsQUtj4ly0WITkBfh%2FzTodhb%2BTNUhSKv7kUBH%2BsWVTxtnNdj91PI4CteKSvqz%2BSp2Z%2FNjJmn26ZFiGhYe57uB%2BGCvdIulR8Jf3Tepr%2F136brhPUNWfVnMW3ukbdBstb2B5g35EsV7RfG5DBHGwFWqj%2FbRRtbmS7Jo8fw4lgXJy%2Bts%2FTf8cWgOLcivnhx0EsAmQlh3PZ%2B9qp1aIUrFtVf%2BrWPzn84w5M5WSAz8fmJSmSkooqYB2qPvMc10AqA%3D%3D&source=SFAPP&bizCode=619
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=UuJZV5PVobA%2B5u0Gvo%2ByRHA2BO95npkDXxobXAjjwuX1%2B5LYkw3arHKujda5%2FJG7k3v90v%2BoKipGDcZg%2BFeeMyJ7fsb0Nvaj14RjnTSpa6R16z8GBVn3yOF28lSDzUo89dwj76QmHffwI2gRlEv0p0gd0aqJ7JjNt8p4k33ey1cjdGniOZuYulJ6b%2B9bPbp9posK5TPkDiTru8WCC3A53TDN15vyl%2BZslPvJt6IT%2FywZkRnRmE4GS0BqIphtF5ht8qXSGxxfGdzzmX6wbBbkeJeZDeZ3wJ2jPjE5fTK%2FttRXyrH1R246Alzkx1hbO7r8wdYvcUmeriBDI6OBzeQUMA%3D%3D&source=SFAPP&bizCode=619
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=FBaUEv0AexehP1O2%2Bs30jJY5NallOEnhRrVuudn8c9zeeMOLo%2BJx9SBq3aagER%2FgEODPrrjjWmJm1jhrmwNyE1BBrtHKKGNvvF%2BC09L%2Be6ptNkK%2Fd6E4%2BwCAfkIcm0XiPNZdfG%2Fk%2F2t6jY9hJlOEu92pv4Y4TBJYEACqV65QD1YnossTZe8p0TVsDOW5tmJGzUNtPcQAq6SdKdVotAZ3irsbLqSH2nmXHw%2FtETw%2FR8U39Mbg7CeEfMQbMo%2BJwJgD%2FsHkcX0W4z9GmPz68AnONl9Mq7VbBSjpsL2FzcQgocAsPr8cjhSL5vwUE5TCHfoVOWN26l5c2XVNi7RZiEoQGA%3D%3D&source=SFAPP&bizCode=619
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=H57snbVFQr6Wsxu3hJtMCqyVAybFUhvpBC07MYompZtGyo26ggHk0yfKrGfDQmrIExudNiKSrrHq60TtMKIrY53WZJICiLXetuitpXn%2FhJqrjBT1mGp5ayXZ45sOnBnJvkeA9B1E%2BqrChXjmb2xaTDmKC1LHVToog%2BXfZzeFEEOUpOekE2aKTsi7WFYL6lrmdvMDunTr5U%2F1BrvqA5y6FjK%2Bmnn%2Fij4PrP1kTTjKwJuslpXTJJJJqRAlhmr43mEmP20ud6ts%2BMUoS4YBzfWkuWS2TabaOCdhOyQM9K6p1rvMDXfg0J7dOGtdS7sygxs2MSSijopWeJTdoKi55nFGeg%3D%3D&source=SFAPP&bizCode=619
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=LqUSPOro9X8voB%2F8DhXtuzVHnvNzK5%2BltsmrgnH1iZR8KoF1Y0jarwGKgPXviHF9czi3kvFr8yt5AHp8RpdE6ge5oB0oPEKvRvUaQ%2FyR2zwUs07alu%2FRb0fBcx5z0MalvmrPsmTVQa%2B9zZ%2BbIVuJSk75I8LILNgN1OYcsnUuN%2BSsqcmMluKk3h055qeyWX7iipV9QJyvq7Z4f9PiTgdyIJG9euBF1phpSd4HgJpcNTe27uS12bX4yA8%2BUaD3vFNAAulIka%2Fauxq2W9z7Re27dMZRdlH3NE6NC9CHvHVMyf5OcoL2wbg%2BkW8022HpBbpQDtMOllWCWYjFH%2Bx3RQpeQw%3D%3D&source=SFAPP&bizCode=619
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=MXWuzv22MroA4DwvncsGtF6N9EeiM8sAP%2ByfLO4U92hFEOoddc45Hdsn2FRgKxo19ODmjl%2BBebyIKDVvJGAw5MAq1wFwiexKhvIw%2FDJO7IsYOGEQulmajK537XLoU6SKKoRqXn%2Bpb6FTygO1n7Aw7eWlDOCOsjBHOW1KBRuvfoLu2usGc7Jis1pVZt7Ydp4bSlfD0pqGzEtLDwhr47VatJryJmhC8%2FzwYTAqVsgufR69PrrbOZK7BsOgYxPLYj1LJ4bjiD2k64s8qnRIPnM75pF%2FqnJCQLd1KfDZfR9ggZxIq5%2FuaqCQVJthZhX6eDcp2Q6cvBmyR6p1h2tLvPD1LA%3D%3D&source=SFAPP&bizCode=619
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=uLVHnTjiRglIFjtiX4EaYZmOWFiCNrbDy88yT0m6iJdeU5l%2BgLEhpxqaGtvymGnpfeNxeZlIjxOVGAg%2FLgZjb%2FzHvtxySlMZdM1%2FXzlUc11s5x8MNPje1ssl7UAO%2FzfGgKHMgRd4YKMGKG7ASaN7lPeNcu3Zf3HFTnzMqQ7QXkolJ6qqYjvuS5OBKTMPkClrlAxm%2BgUv7wxdkRE%2BYGeATBoKfWCTDITtHwM64ZnHEbNZr0pUCnReJgyBCOCF5qc3%2FTEiF20%2B6jxzCmZYatMgCq0lXIU8N47N8VbbrY8O00A51tT06I8745UgA2rO4aIuG5MFLdTtwt7rANqgJOY6SQ%3D%3D&source=SFAPP&bizCode=619
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect?sign=xUC%2BgorfvBVCG1wgOb2GmQ2XVXurC9FHvhs1wyPH9uRVuOWKNrfR1hNaZUco1Byd%2Fo5mMz9BoCufRZgrfN7AvgRwQE0V4VDRsWp4u8%2BaKpNgDvtpPkl55WHEQv7%2BQbHyCcka%2BuBgPtEMuwXWnl%2FhouXl6X4cePUXzlrQi8B6uaNH0A42eFQiwPf6KCNIxvL2wMsOzyZnFjvRFMF7SZIF82GCuSpKMt761VOy6H6EoJr0alRpt4O3dUyYWTZ%2FAAgicX1xujN%2Fv3v3HoHVh8hCHXeSeW8MMvIuaLNcOq8RkHcTYo3Q%2BXvSxKPjZyw6q5FT0vBEKkl%2FLDBRJG0oaCy9SQ%3D%3D&source=SFAPP&bizCode=%7B%22path%22%3A%22%2Fup%2Dmember%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22point240613%22%2C%22categoryCode%22%3A%221%22%7D
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect?sign=JbF78kyq8U41fH4AP0HkTT6OTLQPZScUQiTeeEb659%2FZ17cEcAzxsRG8eBDKM4ArAsl4p6RNIBzbln%2FCp0%2BLdP3%2FINhPbKtADnBLA8xFjfpiXu9aD6L0zbFoQe0p7gC3YyxM21xXNrLk%2Bo%2FEiOgtyS707oFQfzA7MppUBqM9rQAPdYajAz3uwURvseYmbogBojx23VeYWpKzSF%2FV9qJj3UcRIA6c21DCKunG99qc6DB1uxeO2vca%2Beo4xDiQ0yrsyRyNGvjKF%2Bky9lZLDdyvQL8KEKv3uWGpCtim3wUacfAFjOFXU%2B%2F%2BfdPjVN%2FPtn7atgZYJ3%2Fad7T5pOeB5EzsGg%3D%3D&source=SFAPP&bizCode=%7B%22path%22%3A%22%2Fup%2Dmember%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22point240613%22%2C%22categoryCode%22%3A%221%22%7D
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect?sign=YiS0%2BzBrpLkgJ8hqCc1DfEAU5AZ5l2%2FSEtYj%2FarSigavc37iX79KAjhQVYtpkUFTlN0UXWI4QAtr0BCNkaaMWoJJfEpsyf2KY%2B9563QZa%2BpQCFGjfsvTVyPKFYUcaF1MWpukrra0RsmbDwPvEUCEZOUQeNAlDPQ9eAMT1PjgeRR1EnaDUMbRE1vBzKBHiO%2Fe5DErKz0fnSnICF3mbeAumO2g19odtvN1nrcpGuZ2T1JNuE2AKRqoDm4wxMVdVJQyME5a5n%2B1i5rDuwwdN3c2DFT9ZDvZToVIJwZgCFWsA7cNvOh%2FYDVabpMMYvwAshTFVFmzaYbgM4zjuTCjIKqKgQ%3D%3D&source=SFAPP&bizCode=%7B%22path%22%3A%22%2Fup%2Dmember%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22point240613%22%2C%22categoryCode%22%3A%221%22%7D
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect?sign=rIyNMfumIl%2FTVKM7OeTAn4C2igLY%2FtGThN6Iq0Ztg%2F04C%2FC%2B8xbNmkDqcW7oQdPyUOF%2FnOSb2soVdGu5p4ZBcvRMlb1PrbLFV2YTCoijEmniR7Hc0SverDd%2B6LWgIOTlBARPbHwCwh%2FkkJTsfa%2Baj2bsEMdM6gy4Mw1GdG8aydkZP%2Bru9kXMcIoI9MBUYsiTCesRFHpBHl%2B%2BV9py17gjT0n9FdSc8RfEIbZ1jbY1pNwR0aZkUxphjrfaw2Bw8Bv9sP60HmnGjdMvyhp6AhJ19EvF8ruANaRtPFz%2Fn1lXr3GM4xgJoH7S97hilYy5KSMdTGGS%2F%2BimSZU2OQOhOGsjyQ%3D%3D&source=SFAPP&bizCode=%7B%22path%22%3A%22%2Fup%2Dmember%2FnewHome%22%2C%22linkCode%22%3A%22SFAC20230627172106502%22%2C%22supportShare%22%3A%22YES%22%2C%22from%22%3A%22surprise%5Fbenefitappwd%22%2C%22equityKey%22%3A%22surprise%5Fbenefit%22%7D
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect?sign=J0uoidv7UnfNj4laVPvkvBjPKEt8rz2bEql7TEHp4T1NVVd8oYP5rQSsr3tdGk43zRKs6AYZSOMkMsNWiI6eRWT3jjttnfUNW4OgnwnbLc8YMjpW08kUNzLgX5987dSNmS%2FMcGbDB79YX7yhQNf9AuENu%2F2WDYQF9hdhfKO%2FG%2BRU5UhXZq%2FF1nahrJuKzCbiLgiuY1rQJmH%2F7F87Hb9vee1K17GKW7vcYqfmWzQmgEKhNp3yHJYhUt%2F3GtRhhJ2VwjeJAkZ9yMa1%2FqGcw7JJIhNAJXWb2pxc4o8hQBG%2BL4gxpbRQ7DmRf8QOTytdBvaDU4LP%2BC6O%2B9SeYNbdaFooFQ%3D%3D&source=SFAPP&bizCode=%7B%22path%22%3A%22%2Fup%2Dmember%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22point240613%22%2C%22categoryCode%22%3A%221%22%7D
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect?sign=yLQ7O1D7klkwihOc6gtHKZEereyjv%2Bx7tJR3q6p6JCfzXA0rKkv2QxbZnjQZEjcifYyu7kOcfXXK%2FMTcE2j%2BspC0RQFto6VEVIHM%2FNlZplk2nlpXUomtALQs3CRUltwm4GqgK9CqJCvI6vCGMlNAuRwXxjksObkYqNDhXJfm7eT%2FHFWBg51lEh5CwwB7f7a1w2Ncn%2Ft7mGcVjSuWvkfj1r0ywQjA50tdUqDz9k6v4ei%2BkuLFjKpACq%2BGSUb7um769l6XMtnQ%2BkSWOY5dyqDH0W%2FjEs4%2BkCjJOj7JC51yPOHJtgKx9Rh0VJ5Cmdo79%2B%2FI4uGzJlhYPp97kWHJf9f2LQ%3D%3D&source=SFAPP&bizCode=%7B%22path%22%3A%22%2Fup%2Dmember%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22point240613%22%2C%22categoryCode%22%3A%221%22%7D
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect?sign=uQeB04eVSMK2nLjCHbWVOAKvqDrqau6dVvNbP8fqeIAiPKyUL%2FaOZaW4%2Bm70qZNhbx9oeZZrhOrZYhryCE1%2Fe1QqJjVUYFaXqqpY0ZDqPivVR3SPdOyGUJSTdF369bt5wXHlg9Pz5hcDY7cZjphn66kgSSHdGQfwd%2BmiBflExdDZQdIxqn7%2FH9d2qEjbhZPuJYZ9w2mIjP7aZBmwzz6wwwKSgsuKP2ekpcLFf42erIdqePW0bHFnxwPpcl2iNf3RtunVInj8KwIr7ZvF7BORen3Z7DK41NMVK2sJ7Tu6IECOUOaeI%2BK0k4qqNGhTIX2pxEZEm0t6telBti%2FJfsHn0g%3D%3D&source=SFAPP&bizCode=%7B%22path%22%3A%22%2Fup%2Dmember%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22point240613%22%2C%22categoryCode%22%3A%221%22%7D
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/weChat/activityRedirect?source=CX&unionId=DDnNBfAFAHJN1cRq0jRyPYUR%2BV66gcnsVpZVq6ZCzPI%3D&openId=7WTR4uFLN8X2WITyY8karu6mulzI9q%2BYv4Ac6n28Vwg%3D&memId=BVFqxsaFIGz9LGUQIhokeT8dmDMThOKSEN9dNafSsjYDdjSr%2F6X0WoiZtgGzs7sG&memNo=6tB15T6k0ZvyroDMcHJm6dVm5JGXLo1ifFz6xQCH50oDdjSr%2F6X0WoiZtgGzs7sG&mobile=acvWW6aSVh55yXk%2FSa9pmA%3D%3D&mediaCode=wxapp&bizCode=%7B%22path%22%3A%22%2Fup-member%2FnewHome%22%2C%22linkCode%22%3A%22SFAC20230629183611255%22%2C%22supportShare%22%3A%22YES%22%2C%22from%22%3A%22wxwddoudi%22%7D
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect?sign=M3Bk9GfJyMocP%2FX9dfHqPgr2S2ax7B0%2Fu63q0NEyZrgvARCfOAApR2xwSWRr4OJjQhqaAGRyMN06W69VTtgVs55IUEsYGpwEP%2FYkwLocQqTeLIzCv6nhx42LmrpLF9%2BjqK9zBvEKfArrDeWGNola1U4AHA4Swqy8DUWNxOJXU6W1ct%2F5JIWgtIsZS4TCtyPjYK9FhfGdHC2Lq1b5RZhELoHPwvTDKMQATDolXnqYsV4yxIT7%2F%2F5b84%2FR65UxKj3KZPxwY6gtzJpzNivxT0gXOJ2v%2BFaiHQmDry3QTUfYV9%2FsEBLYDG1L%2Bxu3LTrv0tN2G7KpKwixlqbh1GX6rvzq9A%3D%3D&source=SFAPP&bizCode=%7B%22path%22%3A%22%2Fup%2Dmember%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22point240613%22%2C%22categoryCode%22%3A%221%22%7D
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect?sign=gi5gtYlBW9bJUXYi%2Ftqp%2BYxmbHRhUFpGTNy8jayMK9074qGkihS3qV51OWs7OHLBn3%2BMg%2BNj7Bz4EdWEFzRXgk46iWkTU2JR9pwJsi%2F3Y1SrUOm7LuZFEkaxPr3rBbgZ%2FA6LrCGY5OkmLwcD0FNuOgK7hgbC0PEPpBaboswzwUo8EV8PjFHq53PTbpfam4Yk91AZSRgKlGYhJbXaA%2FaGqPuRhT370YS3z3NvwRh4S8duSMhoX%2Bl2srhKydhu4cQs2HsBV6n0TgffstO7XlbI6MZl%2F1hkrEO4R6en6RV5kdmiiwuAtNWKoUVxLVbrF18dtyKQ33%2Bt1qCvgM%2BYl5%2Fvag%3D%3D&source=SFAPP&bizCode=%7B%22path%22%3A%22%2Fup%2Dmember%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22point240613%22%2C%22categoryCode%22%3A%221%22%7D
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect?sign=BjyASq2hGzeD51OxgcGysNgx%2FoY8zjV%2Brb1ISQ3lgXdLDumc%2BevE974uftnCLIKuMjvop2cy%2Fd6tyZhLUpukYbefctCBkPO9OFcRisKMui6GUiWaeVgnG%2FdCRAAykkUv5fiqBYnuX65bLcPWKXTKgTDqfFBjFKEQx8xUO0dVH%2BXR6kdkelcbbJvTVR%2B8nPOlkRyrZ4Le%2FfCaQfIcpL3cSjT3adf64EDKwMLhev0QQ6In8XdT%2B2gRKiWUH%2BcjbaV%2FIOGMeC1qwSNp%2BOZUpoTiHYMgu2Eln%2Bm%2FinoWtZbOR2W1R5v%2B0UWqvUNbny4uwWWjzigU%2F%2FcqD3s5neyCz2xy5A%3D%3D&source=SFAPP&bizCode=%7B%22path%22%3A%22%2Fup%2Dmember%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22point240613%22%2C%22categoryCode%22%3A%221%22%7D
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect?sign=pT5uLmmyPPrsSD8q7TMuYu%2FdOsbUdxrWKAdn0eURcqIQvSKT0pdTHP3q1mU4Jrigp6donq4lTKLzBj6ug1JqGmKHsLFFALZLnDjx6A96JwkjCp0XlTC3%2FgUOCxS0mEKA2CoPrTQaihLn74dtac4QvEKwN%2FboYaO4j8SWc3y6%2FnY7%2FYKuIGhi1nUA9Vu8lFb%2BYUQF9TBpFU3eh5sy3PkTlFcImtOYb4obLhr7O5JchRFlF0WG4CBNz3Cog5ZfUioxTtUc6ucpVnBtp08iP9rMosXHN%2BjkFzX2jb5OwP1UKBJk8jTQisyCT6lluVnS%2B9cc1TSLNavH2ogEmEJ7ZpECJA%3D%3D&source=SFAPP&bizCode=%7B%22path%22%3A%22%2Fup%2Dmember%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22point240613%22%2C%22categoryCode%22%3A%221%22%7D&citycode=021&cityname=%E4%B8%8A%E6%B5%B7
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/weChat/activityRedirect?source=CX&unionId=m0zq5w7xAnJzHt6q9SPDlUila04ciwDWGhcUV4ZxhhQ%3D&openId=SXhVO3xoIWjsgFAVPm9CIU11Oj%2BGbCUjHpgzfP3lyLc%3D&memId=94UfoYjWthqf2N6EbJ8ypsxRQk2vO0oPylYF2YY3XfgDdjSr%2F6X0WoiZtgGzs7sG&memNo=6tB15T6k0ZvyroDMcHJm6QP51om4%2FTDkAv21rjoEvrYDdjSr%2F6X0WoiZtgGzs7sG&mobile=BU5xIChCaOBFLSYriyZvSQ%3D%3D&mediaCode=wxapp&bizCode=%7B%22path%22%3A%22%2Fup-member%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22mypoint%22%2C%22categoryCode%22%3A%221%22%7D&citycode=021&cityname=%E4%B8%8A%E6%B5%B7
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect?sign=Dbo2aqmvwMgw%2BpX%2BEbDfM4BCGGABm11dWmbDNQFUL41CmEi7w8HknM7FbO0Se%2FZBgZOnaw9HZbDuldO770m8zx%2FFe2aQsJW%2BOX3zm2RiBW2Tigy8cRVVaSHasF%2F4vetNI0dB4bo6u8CXArUn39Ggb9yLdd1nAAYvoPrpuMd1ZbNFiclKOtb52Fpi5TNBZMu3LTINZzi5LIRXO3tSROBXSdkVmDQ90Y9ap7%2BAsehM08qhRSGxclAtVcASc0OC%2FOh2YPmmFH17mc2dYzzbOOb%2BU087vsWiBRsb83sw1ekWRWVG9EMzbTmaRB3FCRsn3exv6BzfgUQ302hG6XZLO%3D%3D&source=SFAPP&bizCode=%7B%22path%22%3A%22%Fup%2Dmember%2FnewHome%22%2C%22linkCode%22%3A%22SAC20230627172106502%22%2C%22supportShare%22%3A%22YES%22%2C%22from%22%3A%22surprise%5Fbenefitappwd%22%2C%22quityKey%22%3A%22surprise%5Fbenefit%22%7D&citycode=021&cityname=%E4%B8%8A%E6%B5%B7
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/weChat/activityRedirect?source=CX&unionId=5hQfrcUtYqzottSoC0Q8GeKyossQx6xICC83EVz04jg%3D&openId=xaqyojEdFhM6vPlSSvbRCdWi0oVwrTHdEahantXRDB4%3D&memId=muJt6TZ3jVatgH%2FpEzUgrF4YiodwTbr4Ags7%2BmIUIy0DdjSr%2F6X0WoiZtgGzs7sG&memNo=6tB15T6k0ZvyroDMcHJm6Y0Q7gDUkjysj5lv%2F0xNzucDdjSr%2F6X0WoiZtgGzs7sG&mobile=tKjf4JrQvtkm8QeS3xt3Ig%3D%3D&mediaCode=wxapp&bizCode=%7B%22path%22%3A%22%2Fup-member%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22pointmy2024%22%2C%22categoryCode%22%3A%221%22%7D&citycode=021&cityname=%E4%B8%8A%E6%B5%B7
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/weChat/activityRedirect?source=CX&unionId=gfN5UCebfH7656MEc4OZhJBXFhjuNUoeaZchU1YyYLY%3D&openId=cD2QTqqmr%2FoiXQcGH1jGmgW264iym7Tb5U32Fqo63Cw%3D&memId=yhyJ9M9peJmIjxQUoGo2Pj%2Blf6bshKYyAc6OrziIkpIDdjSr%2F6X0WoiZtgGzs7sG&memNo=6tB15T6k0ZvyroDMcHJm6TpUhPWl7tvjtNUw9jBr%2FpoDdjSr%2F6X0WoiZtgGzs7sG&mobile=38%2FtAADGH4dfp8f0W6qlng%3D%3D&mediaCode=wxapp&bizCode=%7B%22path%22%3A%22%2Fup-member%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22mypoint%22%2C%22categoryCode%22%3A%221%22%7D&citycode=021&cityname=%E4%B8%8A%E6%B5%B7
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/weChat/activityRedirect?source=CX&unionId=dDLe%2FCQLcTwS%2BMTlTHyAYRv2PvbZazlfvW5ATxCrXy8%3D&openId=iApoowZm6%2BcWw8Nfx1igcFF4jjk8qvVI56kGyd9fIH4%3D&memId=YKqjVfhhX6%2FiYUv%2FW2TKi%2BRNagtorgT4sVojgZSw0f8DdjSr%2F6X0WoiZtgGzs7sG&memNo=6tB15T6k0ZvyroDMcHJm6YA3k9mKwIf5e6anrsF0tCMDdjSr%2F6X0WoiZtgGzs7sG&mobile=ees2HhI%2BnGL39tYQig527A%3D%3D&mediaCode=wxapp&bizCode=%7B%22path%22%3A%22%2Fup-member%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22mypoint%22%2C%22categoryCode%22%3A%221%22%7D&citycode=021&cityname=%E4%B8%8A%E6%B5%B7
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/weChat/activityRedirect?source=CX&unionId=J2OmnQLyOHyqn8UsU0nCgVyCTrxDAl8StBPZzmP9kJE%3D&openId=Rf1Cab9rJeJ%2FmyC7sKoYGnvkbHksblOgZ3hAzJSgb30%3D&memId=N9kdzKfLKyLnngzSO6WGss%2BAgnumEOSfxz5FhphgMGwDdjSr%2F6X0WoiZtgGzs7sG&memNo=6tB15T6k0ZvyroDMcHJm6dqNPVWd9SCVS0SQC1w4s5oDdjSr%2F6X0WoiZtgGzs7sG&mobile=K%2BA6CdUUKWZlQc6%2FUf9vMw%3D%3D&mediaCode=wxapp&bizCode=%7B%22path%22%3A%22%2Fup-member%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22mypoint%22%2C%22categoryCode%22%3A%221%22%7D&citycode=021&cityname=%E4%B8%8A%E6%B5%B7
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect?sign=tOCcZED3t4XDYxN%2FDJCMOFnaIY2dDrtWvHfwYT6rq871bhw3svEz8P82kP2KuCNtk8ix9GwsQaAu4wg0m0MVNndpV3n3%2Fo3HPy6gOXXB4w8WGhh7UFurku4H7og9r8Q3b68YncJj7t8i4bmhLL0RptSuJCqSmB5MFA%2BWmDcPWwvTkieaH4Mxyw7bMg9pwSuEUeuT8bmag%2B9dlXYkrHSOCHib57p70z9fI%2FFxNWIY%2Bp9pMm3B8zP7HZXUYVMDbMv2IfsjrIYfp1UIax0%2FyKRCiyp7E14IBgRbrlEOJz4wz61aBgbLZqec3T7gMdx%2BMBJOlexdx2EF%2BbnQWTHDk0xMqg%3D%3D&source=SFAPP&bizCode=%7B%22path%22%3A%22%2Fup%2Dmember%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22point240613%22%2C%22categoryCode%22%3A%221%22%7D&citycode=021&cityname=%E4%B8%8A%E6%B5%B7
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=ajIOz%2Fkrxw7%2FMpVW%2BdwNphszVIKM5RKNg%2BHHPcoErOTEmAEr3csCZ8kLhaR3mdbSA8GGAHTdgCqyXbdolVdrQpnRQFJ99MsC48kpHSlQna%2B3n0B%2FiHwLhwgSyDZeM6qHU6oDMCqwwAx0ibnfOh0uTbPMpWjASPwxjg4OasZQJE9bXmy7C%2BnS4qLM3lhnpJv6wKra7TVuFF9gCOEeLIV5Y2r4CxvPA0qA%2BkhBUyCUA9unQwSIpO2Lk3P626%2BNo8a%2F8w8B%2BadObYB2FPqluJV075TIFzRAOIYhuXaHLYa%2BL0Vpfs7O%2BUv0WAraiORBBGS9ZMuLLT%2Bx2k3bjlK93SMvQA%3D%3D&source=SFAPP&bizCode=692&citycode=021&cityname=%E4%B8%8A%E6%B5%B7
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect?sign=WFDWkuAilDAGJ7VV16E3yfe09x%2FYSV7QkbsVX7S54tjdLIK1%2BMRT6IGRfvt1FTCpW3dCmXYzP3W8Sae5xsG37bHUOey01BQfbUydntpxI2ucITaW5B6i61L4VCPVq%2BlwIWNIlKpc5DHKptrypdcRWUU50vQSdN4UZ%2FLKRlz5Ai1m3Pg%2BhbBnglOtQSbwRJnBenuSPmSbIkVbTXrdRc3pEXFS0bTlkTAKK83Q7DhOal9olVUcVjzpbOqVal3EhYNgkWtUWhjc4fQVf34aXMoimd9PdgCivJVXtVmFLjsGTKtJFCsde0k2uvoHG1nHt%2BpkCseG40X6ccnsv9cA6KRscQ%3D%3D&source=SFAPP&bizCode=%7B%22path%22%3A%22%2Fup%2Dmember%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22point240613%22%2C%22categoryCode%22%3A%221%22%7D&citycode=021&cityname=%E4%B8%8A%E6%B5%B7
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect?sign=hRZXT5ff7uBoSD%2Bbksu3GA5Ha9B6fZXlaj4qVr2r4THLBY1iUtgWoM3EziyHWPO0ukxgwC%2ByuMcuEWLQQswMYOjfo1A7ih89aTWE%2BLlFdjsuvGaipjtFyanPait1pRKUC17CrOwkqZFNBxSCmO5HKSJKAYMjsYvCx2BoTlfCSaXedwpNZWUAfSDQJjC%2Fz2fOKzI62J2vak5jkuvGJUyoR7pFIMvPTrFea%2BxTlfaNwcG8OWQEokNpgZHN%2Fn0nomXzbPRKYNS8hQDyiJhL0qA9WbAJMoWU7PIqstxOTIS52PKn2CT%2BP1mCc2RbTH6smdczYFjfvGqCSgjin%2BtXHAa%2BKQ%3D%3D&source=SFAPP&bizCode=%7B%22path%22%3A%22%2Fup%2Dmember%2FnewPoints%22%2C%22linkCode%22%3A%22SFAC20230803190840424%22%2C%22supportShare%22%3A%22YES%22%2C%22subCategoryCode%22%3A%221%22%2C%22from%22%3A%22point240613%22%2C%22categoryCode%22%3A%221%22%7D&citycode=021&cityname=%E4%B8%8A%E6%B5%B7"""

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

IS_DEV = False

send_msg = ""
one_msg = ""


def Log(cont=""):
    global send_msg, one_msg
    print(cont)
    if cont:
        one_msg += f"{cont}\n"
        send_msg += f"{cont}\n"


# 1905 #0945 #6332 #6615 2559
inviteId = [
    "8C3950A023D942FD93BE9218F5BFB34B",
    "EF94619ED9C84E968C7A88CFB5E0B5DC",
    "9C92BD3D672D4B6EBB7F4A488D020C79",
    "803CF9D1E0734327BDF67CDAE1442B0E",
    "00C81F67BE374041A692FA034847F503",
]


class RUN:
    def __init__(self, info, index):
        global one_msg
        one_msg = ""
        split_info = info.split("@")
        url = split_info[0]
        len_split_info = len(split_info)
        last_info = split_info[len_split_info - 1]
        self.send_UID = None
        if len_split_info > 0 and "UID_" in last_info:
            self.send_UID = last_info
        self.index = index + 1
        Log(f"\n---------开始执行第{self.index}个账号>>>>>")
        self.s = requests.session()

        self.s.verify = False
        self.headers = {
            "Host": "mcs-mimp-web.sf-express.com",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090551) XWEB/6945 Flue",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-language": "zh-CN,zh",
            "platform": "MINI_PROGRAM",
        }
        self.anniversary_black = False
        self.member_day_black = False
        self.member_day_red_packet_drew_today = False
        self.member_day_red_packet_map = {}
        self.login_res = self.login(url)

        self.today = datetime.now().strftime("%Y-%m-%d")
        self.answer = False
        self.max_level = 8
        self.packet_threshold = 1 << (self.max_level - 1)

    def get_deviceId(self, characters="abcdef0123456789"):
        result = ""
        for char in "xxxxxxxx-xxxx-xxxx":
            if char == "x":
                result += random.choice(characters)
            elif char == "X":
                result += random.choice(characters).upper()
            else:
                result += char
        return result

    def login(self, sfurl):
        ress = self.s.get(sfurl, headers=self.headers)
        self.user_id = self.s.cookies.get_dict().get("_login_user_id_", "")
        self.sessionId = self.s.cookies.get_dict().get("sessionId", "")
        self.phone = self.s.cookies.get_dict().get("_login_mobile_", "")
        self.mobile = self.phone[:3] + "*" * 4 + self.phone[7:]
        if self.phone != "":
            Log(f"用户:【{self.phone}】登陆成功")
            return True
        else:
            Log(f"获取用户信息失败")
            return False

    def getSign(self):
        timestamp = str(int(round(time.time() * 1000)))
        token = "wwesldfs29aniversaryvdld29"
        sysCode = "MCS-MIMP-CORE"
        data = f"token={token}&timestamp={timestamp}&sysCode={sysCode}"
        signature = hashlib.md5(data.encode()).hexdigest()
        data = {"sysCode": sysCode, "timestamp": timestamp, "signature": signature}
        self.headers.update(data)
        return data

    def do_request(self, url, data={}, req_type="post"):
        self.getSign()
        try:
            if req_type.lower() == "get":
                response = self.s.get(url, headers=self.headers)
            elif req_type.lower() == "post":
                response = self.s.post(url, headers=self.headers, json=data)
            else:
                raise ValueError("Invalid req_type: %s" % req_type)
            res = response.json()
            return res
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            return None
        except json.JSONDecodeError as e:
            print("JSON decoding failed:", e)
            return None
    def cun(self):
        url="https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~activityCore~deliverOrderService~queryUserOrder"
        result = self.do_request(url)

        if result and result.get("success") and isinstance(result.get("obj"), list) and len(result["obj"]) > 0:
            print(">>>查询到的实物奖励：")
            print(result)
            for item in result["obj"]:
                print(item)
                award_name = item.get("awardName", "未知物品名")
                receiver = item.get("receiver", "未知收件人")
                print(f"物品名称: {award_name}, 收件人: {receiver}")
    def couponList(self):
        print(f">>>>>获取所有优惠卷有效期")
        json_data = {
            "type": "1",
            "pageSize": 10,
            "pageNum": 1,
            "couponType": "",
            "labelCode": "0",
            "channel": "MINI_PROGRAM",
        }
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/coupon/available/list"
        result = self.do_request(url, json_data)
        for coupon in result["obj"]:

            pledgeAmt = coupon.get("pledgeAmt")
            couponType = coupon.get("couponType")
            couponName = coupon.get("couponName")
            invalidTm = coupon.get("invalidTm")
            couponCount = coupon.get("couponNum")

            if int(pledgeAmt) in [8, 10, 12, 15, 16, 20, 23, 30]:
                print(
                    f"优惠卷:{couponName},过期时间:{invalidTm},手机号:{self.phone},优惠金额:{pledgeAmt},数量:{couponCount}"
                )


    def sign(self):
        print(f">>>>>>开始执行签到")
        json_data = {"comeFrom": "vioin", "channelFrom": "WEIXIN"}
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskSignPlusService~automaticSignFetchPackage"
        url2 = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskSignPlusService~queryPointSignAwardList"
        url3 = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskSignPlusService~getUnFetchPointAndDiscount"
        result = self.do_request(url2, data={"channelType": "1"})
        result2 = self.do_request(url3, data={})
        response = self.do_request(url, data=json_data)
        # print(response)
        if response.get("success") == True:
            count_day = response.get("obj", {}).get("countDay", 0)
            if response.get("obj") and response["obj"].get("integralTaskSignPackageVOList"):
                packet_name = response["obj"]["integralTaskSignPackageVOList"][0]["packetName"]
                Log(f">>>签到成功，获得【{packet_name}】，本周累计签到【{count_day + 1}】天")
            else:
                Log(f"今日已签到，本周累计签到【{count_day + 1}】天")
        else:
            print(f'签到失败！原因：{response.get("errorMessage")}')

    def get_SignTaskList(self, END=False):
        if not END:
            print(f">>>开始获取签到任务列表")
        json_data = {
            "channelType": "3",
            "deviceId": self.get_deviceId(),
        }
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskStrategyService~queryPointTaskAndSignFromES"
        response = self.do_request(url, data=json_data)
        # print(response)
        if response.get("success") == True and response.get("obj") != []:
            totalPoint = response["obj"]["totalPoint"]
            if END:
                Log(f"当前积分：【{totalPoint}】")
                return
            Log(f"执行前积分：【{totalPoint}】")
            for task in response["obj"]["taskTitleLevels"]:
                self.taskId = task["taskId"]
                self.taskCode = task["taskCode"]
                self.strategyId = task["strategyId"]
                self.title = task["title"]
                status = task["status"]
                skip_title = ["用行业模板寄件下单", "去新增一个收件偏好", "参与积分活动"]
                if self.title == "领任意生活特权福利":
                    json_data = {"memGrade": 2, "categoryCode": "SHTQ", "showCode": "SHTQWNTJ"}
                    url = (
                        "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberGoods~mallGoodsLifeService~list"
                    )
                    response = self.do_request(url, data=json_data)

                    if response and response.get("success") == True:
                        try:
                            obj_list = response.get("obj", [])
                            found_goods = False

                            for obj_item in obj_list:
                                goodsList = obj_item.get("goodsList", [])
                                if not goodsList:
                                    continue

                                for goods in goodsList:
                                    if goods.get("exchangeStatus") == 1:
                                        self.goodsNo = goods["goodsNo"]
                                        print(f"领取生活权益：当前选择券号：{self.goodsNo}")
                                        self.get_coupom()
                                        found_goods = True
                                        break

                                if found_goods:
                                    break
                            else:
                                print(">没有找到可兑换的商品")

                        except Exception as e:
                            print(f">处理商品列表时出错：{str(e)}")
                    else:
                        print(f'>获取商品列表失败：{response.get("errorMessage") if response else "请求失败"}')
                self.receiveTask()

    def receiveTask(self):
        print(f">>>开始领取【{self.title}】任务奖励")
        json_data = {
            "strategyId": self.strategyId,
            "taskId": self.taskId,
            "taskCode": self.taskCode,
            "deviceId": self.get_deviceId(),
        }
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskStrategyService~fetchIntegral"
        response = self.do_request(url, data=json_data)
        if response.get("success") == True:
            print(f">【{self.title}】任务奖励领取成功！")
        else:
            print(f'>【{self.title}】任务-{response.get("errorMessage")}')

    def do_honeyTask(self):
        # 做任务
        json_data = {"taskCode": self.taskCode}
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberEs~taskRecord~finishTask"
        response = self.do_request(url, data=json_data)
        if response.get("success") == True:
            print(f">【{self.taskType}】任务-已完成")
        else:
            print(f'>【{self.taskType}】任务-{response.get("errorMessage")}')

    def receive_honeyTask(self):
        print(">>>执行收取丰蜜任务")
        # 收取
        self.headers["syscode"] = "MCS-MIMP-CORE"
        self.headers["channel"] = "wxwdsj"
        self.headers["accept"] = "application/json, text/plain, */*"
        self.headers["content-type"] = "application/json;charset=UTF-8"
        self.headers["platform"] = "MINI_PROGRAM"
        json_data = {"taskType": self.taskType}
        # print(json_data)
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~receiveHoney"
        response = self.do_request(url, data=json_data)
        if response.get("success") == True:
            print(f"收取任务【{self.taskType}】成功！")
        else:
            print(f'收取任务【{self.taskType}】失败！原因：{response.get("errorMessage")}')

    def get_coupom(self):
        print(">>>执行领取生活权益领券任务")
        # 领取生活权益领券
        # https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberGoods~pointMallService~createOrder

        json_data = {
            "from": "Point_Mall",
            "orderSource": "POINT_MALL_EXCHANGE",
            "goodsNo": self.goodsNo,
            "quantity": 1,
            "taskCode": self.taskCode,
        }
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberGoods~pointMallService~createOrder"
        response = self.do_request(url, data=json_data)
        if response.get("success") == True:
            print(f">领券成功！")
        else:
            print(f'>领券失败！原因：{response.get("errorMessage")}')

    def get_coupom_list(self):
        print(">>>获取生活权益券列表")
        json_data = {"memGrade": 1, "categoryCode": "SHTQ", "showCode": "SHTQWNTJ"}
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberGoods~mallGoodsLifeService~list"
        response = self.do_request(url, data=json_data)

        if response and response.get("success") == True:
            try:
                obj_list = response.get("obj", [])
                found_goods = False

                for obj_item in obj_list:
                    goodsList = obj_item.get("goodsList", [])
                    if not goodsList:
                        continue

                    for goods in goodsList:
                        if goods.get("exchangeStatus") == 1:
                            self.goodsNo = goods["goodsNo"]
                            print(f"领取生活权益：当前选择券号：{self.goodsNo}")
                            self.get_coupom()
                            found_goods = True
                            break

                    if found_goods:
                        break
                else:
                    print(">没有找到可兑换的商品")

            except Exception as e:
                print(f">处理商品列表时出错：{str(e)}")
            else:
                print(f'>获取商品列表失败：{response.get("errorMessage") if response else "请求失败"}')

    def get_honeyTaskListStart(self):
        print(">>>开始获取采蜜换大礼任务列表")
        # 任务列表
        json_data = {}
        self.headers["channel"] = "wxwdsj"
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~taskDetail"

        response = self.do_request(url, data=json_data)
        # print(response)
        if response.get("success") == True:
            for item in response["obj"]["list"]:
                self.taskType = item["taskType"]
                status = item["status"]
                if status == 3:
                    print(f">【{self.taskType}】-已完成")
                    if self.taskType == "BEES_GAME_TASK_TYPE":
                        self.bee_need_help = False
                    continue
                if "taskCode" in item:
                    self.taskCode = item["taskCode"]
                    if self.taskType == "DAILY_VIP_TASK_TYPE":
                        self.get_coupom_list()
                    else:
                        self.do_honeyTask()
                if self.taskType == "BEES_GAME_TASK_TYPE":
                    self.honey_damaoxian()
                time.sleep(2)

    def honey_damaoxian(self):
        print(">>>执行大冒险任务")
        # 大冒险
        gameNum = 5
        for i in range(1, gameNum):
            json_data = {
                "gatherHoney": 20,
            }
            if gameNum < 0:
                break
            print(f">>开始第{i}次大冒险")
            url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeGameService~gameReport"
            response = self.do_request(url, data=json_data)
            # print(response)
            stu = response.get("success")
            if stu:
                gameNum = response.get("obj")["gameNum"]
                print(f">大冒险成功！剩余次数【{gameNum}】")
                time.sleep(2)
                gameNum -= 1
            elif response.get("errorMessage") == "容量不足":
                print(f"> 需要扩容")
                self.honey_expand()
            else:
                print(f'>大冒险失败！【{response.get("errorMessage")}】')
                break

    def honey_expand(self):
        print(">>>容器扩容")
        # 大冒险
        gameNum = 5

        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~expand"
        response = self.do_request(url, data={})
        # print(response)
        stu = response.get("success", False)
        if stu:
            obj = response.get("obj")
            print(f">成功扩容【{obj}】容量")
        else:
            print(f'>扩容失败！【{response.get("errorMessage")}】')

    def exchange_free(self, ruleCode):
        print(">>>执行兑换23元运费券")
        json_data = {
            "exchangeType": "EXCHANGE_SFC",
            "ruleCode": ruleCode,
        }  # 23yuan的券
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeGiftBagService~exchange"
        response = self.do_request(url, data=json_data)
        print(response)

    def honey_indexData(self, END=False):
        if not END:
            print("\n>>>>>>>开始执行采蜜换大礼任务")
        # 邀请
        random_invite = random.choice([invite for invite in inviteId if invite != self.user_id])
        self.headers["channel"] = "wxwdsj"
        json_data = {"inviteUserId": random_invite}
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~indexData"
        response = self.do_request(url, data=json_data)
        if response.get("success") == True:
            usableHoney = response.get("obj").get("usableHoney")
            if END:
                Log(f"当前丰蜜：【{usableHoney}】")
                return
            Log(f"执行前丰蜜：【{usableHoney}】")
            taskDetail = response.get("obj").get("taskDetail")
            activityEndTime = response.get("obj").get("activityEndTime", "")
            activity_end_time = datetime.strptime(activityEndTime, "%Y-%m-%d %H:%M:%S")

            current_time = datetime.now()

            print(f"当前日期:[{current_time.date()}]")
            if current_time.date() == activity_end_time.date():
                Log("本期活动今日结束，请及时兑换")
                count = usableHoney // 4600 + 2
                print(usableHoney)
                while count > 1:

                    if usableHoney >= 4600:
                        print("执行兑换23元运费")
                        self.exchange_free("RC9038430882584912561")
                        usableHoney -= 4600

                    elif usableHoney < 4600 and usableHoney >= 4000:
                        print("执行兑换20元运费")
                        self.exchange_free("RC9038430882584912390")
                        usableHoney -= 4000

                    elif usableHoney < 4000 and usableHoney >= 3000:
                        print("执行兑换15元运费")
                        self.exchange_free("RC9038431226182306381")
                        usableHoney -= 3000

                    elif usableHoney < 3000 and usableHoney >= 2000:
                        print("执行兑换10元运费")
                        self.exchange_free("RC9038435899106797483")
                        usableHoney -= 2000

                    else:
                        print("可用蜜值不足以继续兑换")
                        break  # 如果可用蜜值不足以兑换，则跳出循环
                count -= 1
            else:
                print(f"本期活动结束时间【{activityEndTime}】")

            if taskDetail != []:
                for task in taskDetail:
                    self.taskType = task["type"]
                    self.receive_honeyTask()
                    time.sleep(2)

    def main(self):
        global one_msg
        wait_time = random.randint(1000, 3000) / 1000.0  # 转换为秒
        time.sleep(wait_time)  # 等待
        one_msg = ""
        if not self.login_res:
            return False
        # 执行签到任务
        self.sign()
        self.get_SignTaskList()
        self.get_SignTaskList(True)

        # 执行丰蜜任务
        self.honey_indexData()
        # 获取任务列表并执行任务
        self.get_honeyTaskListStart()
        self.honey_indexData(True)
        self.couponList()
        self.cun()

if __name__ == "__main__":
    APP_NAME = "顺丰速运"
    ENV_NAME = "SFSY"
    CK_NAME = "url"
    print(
        f"""

✨✨✨ ✨✨✨
    """
    )

    # 分割变量
    if ENV_NAME in os.environ:
        tokens = re.split("@|#|\n", os.environ.get(ENV_NAME))
    elif "sfsyUrl" in os.environ:
        tokens = re.split("@|#|\n", os.environ.get("sfsyUrl"))
    else:
        tokens = [""]
        print(f"无{ENV_NAME}变量")
        # exit()
    # print(tokens)
    if len(tokens) > 0:
        print(f"\n>>>>>>>>>>共获取到{len(tokens)}个账号<<<<<<<<<<")
        for index, infos in enumerate(tokens):
            run_result = RUN(infos, index).main()
            if not run_result:
                continue
