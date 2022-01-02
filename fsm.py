from transitions.extensions import GraphMachine

from utils import send_text_message,send_temp_message,send_carousel_message,send_confirm_message,send_sure_message
from linebot.models import MessageTemplateAction,ImageCarouselColumn,URIAction, MessageAction


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

        
    def is_going_to_menu(self, event):
        text = event.message.text
        return text == '主選單'
    
    def on_enter_menu(self, event):
        title = '拜託選一個啦'
        text = '二選一'
        reply_token = event.reply_token
        btn = [
            MessageTemplateAction(
                label = '喔不痘痘好多',
                text ='痘痘'
            ),
            MessageTemplateAction(
                label = '來促進貨幣流動吧',
                text = '購物'
            ),
        ]
        url = 'https://img.myvideo.net.tw/images/POR010/0000/2038/202007291357297165_2016.jpg'
        send_temp_message(reply_token, title, text, btn, url)

    def is_going_to_back(self, event):
        text = event.message.text
        return text.lower() == "back"

    #Acne
    def is_going_to_acne(self, event):
        text = event.message.text
        return text.lower() == "痘痘"

    def on_enter_acne(self, event):
        reply_token = event.reply_token
        title = '痘痘在哪呢?'
        text = '四選一-選擇一個長痘痘的位置'
        reply_token = event.reply_token
        btn = [
            MessageTemplateAction(
                label = '臉頰',
                text ='臉頰'
            ),
            MessageTemplateAction(
                label = '額頭',
                text = '額頭'
            ),
            MessageTemplateAction(
                label = '下巴',
                text = '下巴'
            ),
            MessageTemplateAction(
                label = '鼻子',
                text = '鼻子'
            ),
        ]
        url = 'https://tse3.mm.bing.net/th?id=OIP.A8vO7O_qBNSybK_fbyOanAHaEJ&pid=Api&P=0&w=289&h=163'
        send_temp_message(reply_token, title, text, btn, url)
        
     #Cheek
    def is_going_to_cheek(self, event):
        text = event.message.text
        return text.lower() == "臉頰"
    
    def on_enter_cheek(self, event):
    
        reply_token = event.reply_token
        send_text_message(reply_token, "長痘原因:\n左臉頰:長痘說明你的血液排毒能力降低，有可能是肝臟出現了問題或是血液循環出現了問題。\n右臉頰:右臉頰長痘是肺部有炎症的反映。\n請輸入 '下一步 '")
        
    #chin
    def is_going_to_chin(self, event):
        text = event.message.text
        return text.lower() == "下巴"
    
    def on_enter_chin(self, event):
    
        reply_token = event.reply_token
        send_text_message(reply_token, "長痘原因:\n主要是因為體內激素分泌旺盛，尤其在女生經期前後會更受到影響。\n請輸入 '下一步 '")
        
    #forehead
    def is_going_to_forehead(self, event):
        text = event.message.text
        return text.lower() == "額頭"
    
    def on_enter_forehead(self, event):
    
        reply_token = event.reply_token
        send_text_message(reply_token, "長痘原因:\n不規律的作息、情緒不佳或是壓力過大，進而導致肝臟累積過多毒素，是額頭冒痘的最大原因\n請輸入 '下一步 '")
     
    #nose   
    def is_going_to_nose(self, event):
        text = event.message.text
        return text.lower() == "鼻子"
    
    def on_enter_nose(self, event):
    
        reply_token = event.reply_token
        send_text_message(reply_token, "長痘原因:\n皮脂分泌過多，循環系統不好，或是消化不良、胃不好、便秘等原因\n請輸入 '下一步 '")
    
    
     #solve
    def is_going_to_solve(self, event):
        text = event.message.text
        return text.lower() == "前往"
    
    def on_enter_solve(self, event):
        reply_token = event.reply_token
        title='請支援痘痘'
        col=[
            ImageCarouselColumn(
                         image_url='https://tse1.mm.bing.net/th?id=OIP.P3jzV_BP52idR336NjQqeQHaEn&pid=Api&P=0&w=261&h=164',
                         action=URIAction(
                             label='痘痘藥推薦',
                             uri='https://beauty-upgrade.tw/49441/'
                         )
            ),
            ImageCarouselColumn(
                         image_url='https://tse2.mm.bing.net/th?id=OIP.y82ZcKI2xafVn-QrGXNEDAHaFj&pid=Api&P=0&w=230&h=173',
                         action=URIAction(
                             label='診所推薦',
                             uri='https://www.ptt.cc/bbs/BeautySalon/M.1422581205.A.AF9.html'
                         )
             )
        ]
        send_carousel_message(reply_token,title,col)
        self.go_back()
    
    #through
    def is_going_to_through(self, event):
        text = event.message.text
        return text.lower() == "下一步"
    
    def on_enter_through(self, event):
    
        reply_token = event.reply_token
        text="check"
        title="要瞭解解決辦法嗎?"
        col=[
             MessageAction(
                 label='前往',
                 text='前往',
             ),
             MessageAction(
                 label='返回',
                 text='主選單',
             )
        ]
        send_confirm_message(reply_token,text,title,col)
    
    #shopping
    def is_going_to_shopping(self, event):
        text = event.message.text
        return text.lower() == "購物"

    def on_enter_shopping(self, event):

        reply_token = event.reply_token
        title='購物連結'
        col=[
            ImageCarouselColumn(
                         image_url='https://tse1.mm.bing.net/th?id=OIP.twb-dr7Gw20BarEFoO1n_AHaD3&pid=Api&P=0&w=314&h=165',
                         action=URIAction(
                             label='點我進入蝦皮',
                             uri='https://shopee.tw/'
                         )
            ),
            ImageCarouselColumn(
                         image_url='https://tse4.mm.bing.net/th?id=OIP.K-twQDK0Aa45NsA3BUl3igAAAA&pid=Api&P=0&w=300&h=300',
                         action=URIAction(
                             label='點我進入PChome',
                             uri='https://24h.pchome.com.tw/'
                         )
             )
        ]
        send_carousel_message(reply_token,title,col)
        self.go_back()
    
     #sure  
    def is_going_to_sure(self, event):
        text = event.message.text
        return text.lower() == "購物"
    
    def on_enter_sure(self, event):
    
        reply_token = event.reply_token
        send_sure_message(reply_token)

        