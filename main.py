import flet as ft
import math

def main(page: ft.Page):
    # App ၏ ခေါင်းစဉ်နှင့် အသွင်အပြင် သတ်မှတ်ခြင်း
    page.title = "Steel1 - Kobelco RK250 Smart Planner"
    page.scroll = "adaptive"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # ခေါင်းစဉ် စာသား
    title_text = ft.Text("Steel1", size=26, weight="bold", color="blue")
    subtitle_text = ft.Text("Ultimate Smart Lift Planner (Kobelco RK250)", size=16, italic=True)

    # 1. Database (အချက်အလက်အသစ်များ အကုန်ဖြည့်သွင်းထားပါသည်)
    crane_database = {
        6.3: {
            "360": {
                9.32:  {3.0: 25.0, 4.0: 23.0, 5.0: 19.4, 6.0: 16.3},
                16.42: {5.0: 16.7, 8.0: 10.9, 10.0: 7.4, 12.0: 5.45},
                23.52: {6.0: 11.2, 10.0: 7.05, 14.0: 4.15, 16.0: 3.45},
                30.62: {8.0: 7.0, 12.0: 4.95, 16.0: 3.15, 20.0: 1.9, 24.0: 1.15}
            }
        },
        5.1: {
            "front": {
                9.32:  {3.0: 25.0, 4.0: 23.0, 5.0: 19.4, 6.0: 16.3},
                16.42: {5.0: 16.7, 8.0: 10.9, 10.0: 7.4, 12.0: 5.45},
                23.52: {6.0: 11.2, 10.0: 7.05, 14.0: 4.15, 16.0: 3.45},
                30.62: {8.0: 7.0, 12.0: 4.95, 16.0: 3.15, 20.0: 1.9, 24.0: 1.15}
            },
            "side": {
                9.32:  {3.0: 25.0, 4.0: 23.0, 5.0: 18.1, 6.0: 12.9},
                16.42: {5.0: 15.6, 8.0: 9.65, 10.0: 6.20, 12.0: 4.30},
                23.52: {6.0: 11.2, 10.0: 6.90, 14.0: 3.75, 16.0: 2.80},
                30.62: {8.0: 7.0, 12.0: 4.90, 16.0: 3.00, 20.0: 1.65, 24.0: 0.90}
            }
        }
    }
    single_line_pull = 3.5

    # 2. အသုံးပြုသူ ထည့်သွင်းရန် အကွက်များ (Inputs)
    outrigger_dropdown = ft.Dropdown(
        label="Outrigger အကျယ် (m)",
        options=[ft.dropdown.Option("6.3"), ft.dropdown.Option("5.1")],
        width=250
    )
    
    area_dropdown = ft.Dropdown(
        label="အလုပ်လုပ်မည့် ဧရိယာ ('360', 'front', 'side')",
        options=[ft.dropdown.Option("360"), ft.dropdown.Option("front"), ft.dropdown.Option("side")],
        width=250
    )
    
    radius_input = ft.TextField(label="Operating Radius (မီတာ)", width=250, keyboard_type="number")
    load_input = ft.TextField(label="မချီမည့် ဝန် (တန်)", width=250, keyboard_type="number")
    parts_input = ft.TextField(label="ကြိုးအရေအတွက် (Parts of Line)", width=250, keyboard_type="number")

    # 3. အဖြေပြသမည့် နေရာ (Output)
    result_text = ft.Text("", size=15, weight="bold")

    # 4. တွက်ချက်မည့် လုပ်ဆောင်ချက် (Function)
    def calculate_logic(e):
        try:
            out_val = float(outrigger_dropdown.value)
            area_val = area_dropdown.value.lower()
            rad_val = float(radius_input.value)
            load_val = float(load_input.value)
            parts_val = int(parts_input.value)
            
            rope_capacity = parts_val * single_line_pull
            found_option = False
            result_output = "📊 စစ်ဆေးမှု ရလဒ်များ:\n" + "-"*35 + "\n"

            # အမှားစစ်ဆေးခြင်း (Validation)
            if out_val == 6.3 and area_val != "360":
                result_text.value = "⚠️ [Error] Outrigger 6.3m တွင် ဧရိယာကို '360' သာ ရွေးချယ်ပေးပါ။"
                result_text.color = "orange"
                page.update()
                return
            elif out_val == 5.1 and area_val == "360":
                result_text.value = "⚠️ [Error] Outrigger 5.1m တွင် 'front' သို့မဟုတ် 'side' သာ ရွေးချယ်ပေးပါ။"
                result_text.color = "orange"
                page.update()
                return

            if out_val in crane_database and area_val in crane_database[out_val]:
                available_booms = crane_database[out_val][area_val]
                
                for boom_length, capacities in available_booms.items():
                    if rad_val < boom_length and rad_val in capacities:
                        chart_capacity = capacities[rad_val]
                        actual_max_load = min(chart_capacity, rope_capacity)
                        
                        if actual_max_load >= load_val:
                            found_option = True
                            angle_deg = math.degrees(math.acos(rad_val / boom_length))
                            
                            result_output += f"✅ Boom {boom_length}m ကို အသုံးပြုနိုင်ပါသည်။\n"
                            result_output += f"   - Boom မြှင့်ရမည့်ထောင့်: ခန့်မှန်းခြေ {angle_deg:.1f}°\n"
                            if chart_capacity > rope_capacity:
                                result_output += f"   - သတိပြုရန်: ဇယားအရ {chart_capacity} တန်ရသော်လည်း ကြိုး {parts_val} ကြိုးဖြင့် အများဆုံး {actual_max_load} တန်သာ ချီခွင့်ပြုပါသည်။\n\n"
                            else:
                                result_output += f"   - ဤအနေအထားတွင် အများဆုံး {actual_max_load} တန်အထိ ချီနိုင်ပါသည်။\n\n"
            
            if not found_option:
                result_output += "❌ [အန္တရာယ် / မဖြစ်နိုင်ပါ] သင်ပေးထားသော အချက်အလက်များဖြင့် ဘေးကင်းစွာ ချီမနိုင်မည့် အနေအထား မတွေ့ရှိပါ။\n"
                result_output += "💡 အကြံပြုချက် - ကြိုး (Parts of Line) ထပ်ထိုးရန်၊ Outrigger ထပ်ထုတ်ရန် (သို့) ပိုကြီးသော ကရိန်း လိုအပ်နိုင်ပါသည်။"
                result_text.color = "red"
            else:
                result_text.color = "green"
                
            result_text.value = result_output
            
        except Exception as ex:
            result_text.value = "ကျေးဇူးပြု၍ အချက်အလက်များကို ပြည့်စုံမှန်ကန်စွာ ထည့်သွင်းပါ။"
            result_text.color = "red"
            
        page.update()

    # 5. တွက်ချက်ရန် ခလုတ် (Button)
    calc_button = ft.ElevatedButton("စစ်ဆေးမည် (Calculate)", on_click=calculate_logic, bgcolor="blue", color="white")

    # 6. ဖန်တီးထားသည်များကို App စခရင်ပေါ်သို့ တင်ခြင်း
    page.add(
        title_text,
        subtitle_text,
        ft.Divider(),
        outrigger_dropdown,
        area_dropdown,
        radius_input,
        load_input,
        parts_input,
        ft.Container(height=10), # မှားနေသော VerticalDivider နေရာတွင် ပြင်ဆင်ထားပါသည်
        calc_button,
        ft.Divider(),
        result_text
    )

# App ကို စတင် Run ခြင်း
ft.app(target=main)

