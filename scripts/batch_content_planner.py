#!/usr/bin/env python3
"""
Bộ tạo kế hoạch nội dung tự động (Batch Content Planner) 30 ngày cho KOL Nhun Nhun.
Định dạng: Độc thoại chính diện (FaceTime monologue), hài hước, tự trào, giữ chân cao.
Tuyệt đối không bán hàng lộ liễu.
"""

import json
from pathlib import Path

TOPICS = [
    {
        "id": "TOPIC_01",
        "title": "Thứ khó buông bỏ nhất",
        "category": "Relatable Humor",
        "script": "Hồi xưa em tưởng thứ khó buông nhất là tình cảm, chia tay là khóc mấy ngày mấy đêm! Ai ngờ đâu thứ khó buông nhất cuộc đời này... là cái điện thoại! Miệng bảo đi ngủ sớm cho đẹp da, mà mở mắt ra là ba giờ sáng! Còn mấy bà, thứ khó buông nhất của mấy bà bây giờ là cái gì?",
        "veo_prompt_shot1": "Cinematic portrait of a charming 22yo Vietnamese girl with cute bob haircut, see-through bangs, wearing a grey newsboy baker boy cap and cozy white knit sweater, sitting in cozy wooden aesthetic cafe, looking candidly into front phone camera, smiling playfully, talking expressively, soft daylight bokeh background, 4k 60fps",
        "veo_prompt_shot2": "Cinematic close-up portrait of the same charming 22yo Vietnamese girl with cute bob haircut, see-through bangs, wearing grey newsboy baker boy cap, holding smartphone candidly, laughing playfully and shaking head, looking directly into camera with bright expressive eyes, warm cafe lighting, 4k 60fps",
        "call_to_comment": "Thứ khó buông nhất của mấy bà bây giờ là cái gì?"
    },
    {
        "id": "TOPIC_02",
        "title": "Nghịch lý giảm cân thứ Hai",
        "category": "Relatable Humor",
        "script": "Cứ mỗi tối Chủ nhật là em tự hứa với lòng: 'Thứ Hai tuần này nhất định mình phải ăn uống healthy để lấy lại vóc dáng!' Nhưng mà mấy bà biết không, cái thứ Hai nó lạ lắm! Vừa mở mắt ra đi làm một cái là trà sữa full topping nó tự nhảy vào giỏ hàng hồi nào không hay! Ai có cái nết giảm cân giống em hông?",
        "veo_prompt_shot1": "Cinematic portrait of charming 22yo Vietnamese girl with cute bob hair, see-through bangs, wearing oversized warm beige cardigan, sitting at cafe desk, making serious determined face then suddenly laughing cutely, front camera angle, warm lighting, 4k",
        "veo_prompt_shot2": "Cinematic close-up portrait of the same 22yo girl holding an aesthetic milk tea cup, giggling sheepishly and covering mouth with hand, looking playfully at camera, 4k 60fps",
        "call_to_comment": "Có ai thứ Hai nào cũng thề giảm cân như em hông?"
    },
    {
        "id": "TOPIC_03",
        "title": "Quy luật 5 phút buổi sáng",
        "category": "Relatable Humor",
        "script": "Trên đời này có một bí ẩn khoa học mà không ai giải thích được: Đó là '5 phút ngủ nướng' buổi sáng! Mình chỉ vừa nhắm mắt xin thêm đúng 5 phút thôi, mà mở mắt ra một cái là đồng hồ đã nhảy hẳn 45 phút! Xong rồi cuốn cuồng lên chạy như một vị thần! Có ai sáng nào cũng trải qua cảm giác đau tim này không?",
        "veo_prompt_shot1": "Cinematic portrait of cute 22yo Vietnamese girl with messy cute bob hair, wearing fluffy pastel hoodie, rubbing eyes sleepy then suddenly making shocked wide-eyed expression, natural morning sunlight, 4k",
        "veo_prompt_shot2": "Cinematic close-up of the same girl shaking her head and laughing at herself, pointing at camera playfully, 4k",
        "call_to_comment": "Kỷ lục ngủ nướng lố giờ của mấy bà là bao nhiêu phút?"
    },
    {
        "id": "TOPIC_04",
        "title": "Nỗi khổ kẻ eyeliner hai bên",
        "category": "Girlhood & Glow-up",
        "script": "Con gái tụi em có một nỗi ám ảnh kinh hoàng mang tên: Kẻ mắt eyeliner! Bên trái thì cong vút sắc lẹm chuẩn tỉ lệ vàng, tới lượt vẽ bên phải một cái là nó biến thành hình con giun luôn! Thế là đồ thêm một chút, đồ qua đồ lại, cuối cùng biến thành gấu trúc luôn! Mấy bà kẻ eyeliner mất bao lâu vậy?",
        "veo_prompt_shot1": "Cinematic portrait of 22yo Vietnamese girl with cute bob hair and grey beret, holding an eyeliner pen near face, squinting concentrate then frowning cutely, front camera vlog style, 4k",
        "veo_prompt_shot2": "Cinematic close-up of the same girl smiling with an amused self-deprecating face, pointing to her winged eyeliner playfully, 4k 60fps",
        "call_to_comment": "Bình thường mấy bà kẻ mắt mất bao nhiêu phút?"
    },
    {
        "id": "TOPIC_05",
        "title": "Người yêu cũ nhắn tin chúc sinh nhật",
        "category": "Dating & Life Thoughts",
        "script": "Tự nhiên 12 giờ đêm sinh nhật, thấy tin nhắn 'Chúc em sinh nhật vui vẻ, hạnh phúc nhé' từ nick người yêu cũ! Trong đầu em kiểu: ủa anh ơi, chia tay 3 năm trời không một lời hỏi han, tự nhiên canh đúng nửa đêm gửi chi vậy? Theo mấy bà, trường hợp này nên 'Đã xem' hay bấm 'Cảm ơn anh' cho lịch sự nè?",
        "veo_prompt_shot1": "Cinematic portrait of charming 22yo Vietnamese girl sitting in aesthetic room with fairy lights, looking curiously at phone screen with furrowed brows then looking up at camera with amused smirk, 4k",
        "veo_prompt_shot2": "Cinematic close-up of the same girl gesturing with hands expressively, asking camera playfully, warm cozy vibe, 4k",
        "call_to_comment": "Là mấy bà thì có rep tin nhắn này hông?"
    }
]

def main():
    output_file = Path('/root/nhunnhun/assets/content_calendar_sample.json')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(TOPICS, f, indent=2, ensure_ascii=False)
    print(f"Đã tạo kế hoạch nội dung mẫu tại: {output_file}")

if __name__ == '__main__':
    main()
