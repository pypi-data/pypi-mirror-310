from DrissionPage import Chromium, ChromiumOptions
import json, re, threading, random



class give_me_a_chance():
    def __init__(self, url, info):
        self.info = info
        co = ChromiumOptions().auto_port()
        # co = co.headless()
        if info["姓名"] == "杨鸿强":
            co.set_argument('--start-maximized')
        br = Chromium(co, session_options=False)
        tab = br.latest_tab

        tab.set.cookies.clear()
        tab.get(url)
        tab.set.cookies.clear()

        # submit_btn = tab.ele("css:#SubmitBtnGroup", timeout=1)
        fieldset = tab.ele('t:fieldset')

        if not fieldset:
            count_down = tab.ele('#divStartTimeTip')
            # 距离开始还有0天0时21分4秒
            start_time = re.match(r"距离开始还有(\d+)天(\d+)时(\d+)分(\d+)秒", count_down.text)
            # 转换为秒
            start_time = int(start_time.group(1)) * 24 * 60 * 60 + int(start_time.group(2)) * 60 * 60 + int(start_time.group(3)) * 60 + int(start_time.group(4))

            while True:
                print(f"等待{start_time}秒", end="\r")
                tab.wait(1)
                start_time -= 1
                if start_time <= 0:
                    break

            tab.refresh()

        # tab.ele('css:.layui-layer-btn1').click()
        fieldset = tab.ele('t:fieldset')

        fields = fieldset.eles('css:>div')

        for i in fields:
            field_label = i.ele('.field-label').ele('.topichtml')

            ans = self.match(field_label.text)

            field_label_type = i.attr('type')
            if field_label_type == "1": # 输入框
                ui_input_text = i.ele('.ui-input-text').ele('t:input')
                ui_input_text.input(ans)
            elif field_label_type == "3": # 单选按钮
                radios = i.eles(".ui-radio")
                for i in radios:
                    # self.match_ans(ans, i.text)
                    if i.text == ans:
                        i.click()
                        break
            elif field_label_type == "7": # 下拉框
                ui_select = i.ele('.ui-select').ele('t:select')
                ui_select.select(ans)
        
        tab.ele("css:#SubmitBtnGroup").click()
        tab.get_screenshot(name=f"{info['姓名']}",full_page=True)
        
        layui_btn0 = tab.ele(".layui-layer-btn0", timeout=0.3)
        if layui_btn0:
            layui_btn0.click()
            print("按下确认")

        captcha = tab.ele("#captcha")
        if captcha and captcha.style("display") == "block":
            tab.ele("#captchaOut").click()
            print("智能验证")

        slider = tab.ele("#nc_1_n1z")
        if slider:
            slider.drag_to(tab.ele("#SM_POP_CLOSE_1"))
            print("滑动验证")

        refresh_btn = tab.ele("#nc_1_refresh1", timeout=0.3)
        if refresh_btn:
            refresh_btn.click()
            print("刷新验证")
            slider = tab.ele("#nc_1_n1z", timeout=1)
            if slider:
                slider.drag_to(tab.ele("#SM_POP_CLOSE_1", timeout=1))
                print("滑动验证")
        
        submit_btn = tab.ele("css:#SubmitBtnGroup")
        if submit_btn:
            submit_btn.click()
            tab.get_screenshot(name=f"{info['姓名']}",full_page=True)

        complete = tab.ele(".completeWrap")
        if complete:
            tab.close()
            br.quit()

    def match(self, question)->str:
        xm = re.compile(r".*姓名.*")
        xh = re.compile(r".*学号.*")
        xy = re.compile(r".*学院.*")
        nj = re.compile(r".*年级.*")
        zy = re.compile(r".*专业.*")
        dh = re.compile(r".*(?:电话|手机|联系方式).*")
        tw = re.compile(r".*(?:问题|提问|回答|互动).*")
        xb = re.compile(r".*(?:性别|男|女).*")
        if xm.match(question):
            return self.info["姓名"]
        elif xh.match(question):
            return self.info["学号"]
        elif xy.match(question):
            return self.info["学院"]
        elif nj.match(question):
            return self.info["年级"]
        elif zy.match(question):
            return self.info["专业"]
        elif dh.match(question):
            return self.info["电话"]
        elif tw.match(question):
            return self.info["提问"]
        elif xb.match(question):
            return self.info["性别"]
        else:
            return ""

    def match_ans(self, ans, choice) -> bool:
        pass
        

if __name__ == '__main__':
    url = "https://www.wjx.cn/vm/PWzc6Mu.aspx"
    
    with open("info.json", "r", encoding="utf-8") as f:
        info = json.load(f)

    import time
    # 多线程，同时操作多个浏览器
    for i in info:
        threading.Thread(target=give_me_a_chance, args=(url, i)).start()