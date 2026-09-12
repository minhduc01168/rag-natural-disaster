"""
Doc 1 Benchmark Data (TERRA_QA_001 -> TERRA_QA_012)
Source: filtered_pdf_markdown/0575f59d64e3407fa40049196cd01c5d.md
"""

DOC1_ITEMS = [
    {
        "id": "TERRA_QA_001",
        "source_document": "0575f59d64e3407fa40049196cd01c5d.md",
        "category": "risk_assessment_mapping",
        "sub_category": "Định nghĩa và phân loại hiểm họa",
        "difficulty": "easy",
        "question": "Theo tài liệu tập huấn phòng chống thiên tai, hiểm họa được định nghĩa như thế nào?",
        "ground_truth_context": "Là bất kỳ sự kiện, hiện tượng (do tự nhiên hoặc con người) có khả năng gây tổn thất đến tính mạng, tài sản và đời sống, gây thiệt hại về kinh tế, xã hội và tàn phá môi trường.\n\n> [MÔ TẢ HÌNH ẢNH]: Hình ảnh minh họa một khu vực ven biển với những vách đá và cây cối. Phía dưới là bãi biển với một số người đang đi lại gần những ngôi nhà nhỏ. Bầu trời có mây, và biển có sóng. Hình ảnh này có thể đại diện cho một hiểm họa tự nhiên tiềm tàng hoặc một khu vực dễ bị ảnh hưởng bởi các hiện tượng thời tiết.\n\nVí dụ: Bão, áp thấp nhiệt đới, lũ lụt, lốc...",
        "ground_truth_answer": "Hiểm họa là bất kỳ sự kiện, hiện tượng (do tự nhiên hoặc con người gây ra) có khả năng gây tổn thất đến tính mạng, tài sản, đời sống, gây thiệt hại về kinh tế, xã hội và tàn phá môi trường (ví dụ như bão, áp thấp nhiệt đới, lũ lụt, lốc xoáy...).",
        "keywords": ["hiểm họa", "định nghĩa", "tự nhiên", "con người", "tổn thất", "bão lũ"]
    },
    {
        "id": "TERRA_QA_002",
        "source_document": "0575f59d64e3407fa40049196cd01c5d.md",
        "category": "risk_assessment_mapping",
        "sub_category": "Phân biệt hiểm họa và thảm họa",
        "difficulty": "easy",
        "question": "Khi nào một hiện tượng hiểm họa thiên nhiên sẽ trở thành một thảm họa?",
        "ground_truth_context": "Hiểm hoạ sẽ trở thành thảm hoạ khi chúng xảy ra ở những nơi có nhiều người sinh sống, hoạt động và gây ra thiệt hại về tính mạng, tài sản và cuộc sống con người.\n\n> [MÔ TẢ HÌNH ẢNH]: Hình ảnh minh họa một khu vực ven biển bị tàn phá. Có nhiều tảng đá lớn nằm rải rác trên bãi biển, cây cối bị đổ hoặc trơ trụi. Cảnh quan trông hoang tàn và bị hư hại nặng nề, gợi lên hậu quả của một thảm họa tự nhiên như bão hoặc lũ lụt.\n\nVí dụ: Trong bão, lũ lụt có nhiều người chết, bị thương, tài sản gia súc gia cầm bị cuốn trôi.",
        "ground_truth_answer": "Hiểm họa sẽ trở thành thảm họa khi chúng xảy ra ở những nơi có nhiều người sinh sống, hoạt động và gây ra thiệt hại thực tế về tính mạng, tài sản và đời sống con người (ví dụ: bão lũ làm chết, bị thương nhiều người, cuốn trôi gia súc và nhà cửa).",
        "keywords": ["thảm họa", "hiểm họa", "người sinh sống", "thiệt hại", "tính mạng", "tài sản"]
    },
    {
        "id": "TERRA_QA_003",
        "source_document": "0575f59d64e3407fa40049196cd01c5d.md",
        "category": "typhoon_flood",
        "sub_category": "Phân cấp bão và áp thấp nhiệt đới",
        "difficulty": "easy",
        "question": "Áp thấp nhiệt đới và bão được phân biệt với nhau như thế nào dựa trên cấp gió?",
        "ground_truth_context": "Áp thấp nhiệt đới là một xoáy thuận nhiệt đới có sức gió mạnh nhất từ cấp 6 đến cấp 7 và có thể có gió giật.\n\n#### 2.1.2. Bão:\n\nBão là một xoáy thuận nhiệt đới có sức gió mạnh từ cấp 8 trở lên và có thể có gió giật.",
        "ground_truth_answer": "Áp thấp nhiệt đới là xoáy thuận nhiệt đới có sức gió mạnh nhất từ cấp 6 đến cấp 7 (kèm gió giật). Trong khi đó, bão là xoáy thuận nhiệt đới có sức gió mạnh từ cấp 8 trở lên và có thể có gió giật.",
        "keywords": ["áp thấp nhiệt đới", "bão", "sức gió", "cấp 6", "cấp 7", "cấp 8", "xoáy thuận nhiệt đới"]
    },
    {
        "id": "TERRA_QA_004",
        "source_document": "0575f59d64e3407fa40049196cd01c5d.md",
        "category": "typhoon_flood",
        "sub_category": "Phân loại cấp bão theo thang Beaufort",
        "difficulty": "medium",
        "question": "Các cấp độ bão mạnh và rất mạnh theo quy chuẩn khí tượng được xác định từ cấp gió nào?",
        "ground_truth_context": "Hiện nay, theo bảng xếp hạng Beaufort, bão được thêm vào từ cấp 13 đến cấp 17.\n- Bão từ cấp 10 - cấp 11 gọi là bão mạnh.\n- Từ cấp 12 trở lên được gọi là bão rất mạnh.\n- Bão đổ bộ là tâm bão đã vào đất liền.\n- Bão tan là bão đã suy yếu thành vùng áp thấp, sức gió mạnh nhất dưới cấp 6.",
        "ground_truth_answer": "Theo bảng xếp hạng, bão từ cấp 10 đến cấp 11 được gọi là bão mạnh; bão từ cấp 12 trở lên được gọi là bão rất mạnh. Bão tan khi đã suy yếu thành vùng áp thấp có sức gió mạnh nhất dưới cấp 6.",
        "keywords": ["bão mạnh", "bão rất mạnh", "cấp 10", "cấp 11", "cấp 12", "bão tan", "Beaufort"]
    },
    {
        "id": "TERRA_QA_005",
        "source_document": "0575f59d64e3407fa40049196cd01c5d.md",
        "category": "landslide_flashflood",
        "sub_category": "Nhận diện các loại lũ và cơ chế lũ quét",
        "difficulty": "medium",
        "question": "Có mấy loại lũ chính và lũ quét ở miền núi hình thành do những nguyên nhân nào?",
        "ground_truth_context": "# Có ba loại lũ chính:\n## * Lũ quét:\n*   Thường xảy ra trên các sông suối ở miền núi\n*   Do các trận mưa lớn ở những vùng có độ dốc cao, cây cối bị phá huỷ đất không còn khả năng giữ nước\n*   Diễn ra trong thời gian ngắn, dòng nước chảy xiết, xuất hiện nhanh, khó dự báo trước lũ quét xảy ra ở đâu\n*   Lũ quét có thể xảy ra khi vỡ hồ, đập",
        "ground_truth_answer": "Có 3 loại lũ chính: lũ quét, lũ sông và lũ ven biển. Lũ quét thường xảy ra ở sông suối miền núi do mưa lớn ở vùng độ dốc cao, thảm thực vật bị phá hủy khiến đất mất khả năng giữ nước, hoặc do sự cố vỡ hồ, đập. Lũ quét xuất hiện rất nhanh, dòng chảy xiết trong thời gian ngắn và rất khó dự báo vị trí chính xác.",
        "keywords": ["ba loại lũ", "lũ quét", "miền núi", "độ dốc cao", "mất rừng", "vỡ đập", "chảy xiết"]
    },
    {
        "id": "TERRA_QA_006",
        "source_document": "0575f59d64e3407fa40049196cd01c5d.md",
        "category": "first_aid_survival",
        "sub_category": "Nguyên tắc chằng chống nhà trước bão",
        "difficulty": "medium",
        "question": "Những nguyên tắc an toàn bắt buộc phải tuân thủ khi thực hiện chằng chống nhà cửa trước mùa mưa bão là gì?",
        "ground_truth_context": "## 2. Nguyên tắc:\n- Phải tự bảo vệ mình và những người xung quanh.\n- Phải có đầy đủ các trang thiết bị bảo hộ cá nhân.\n- Phải cần có sự giúp đỡ của người khác.\n- Phải chuẩn bị đầy đủ các vật dụng rồi mới làm.\n- Tắt cầu dao điện trước khi chằng nhà\n- Chằng nhà trước khi bão xảy ra.",
        "ground_truth_answer": "Các nguyên tắc an toàn gồm: (1) Tự bảo vệ mình và người xung quanh; (2) Có đầy đủ trang thiết bị bảo hộ cá nhân; (3) Phải có người hỗ trợ, giúp đỡ; (4) Chuẩn bị đủ dụng cụ, vật liệu trước khi bắt đầu; (5) Tắt cầu dao điện trước khi chằng chống; (6) Hoàn thành chằng chống nhà trước khi bão đổ bộ.",
        "keywords": ["chằng chống nhà", "nguyên tắc", "tắt cầu dao", "trang thiết bị bảo hộ", "trước khi bão"]
    },
    {
        "id": "TERRA_QA_007",
        "source_document": "0575f59d64e3407fa40049196cd01c5d.md",
        "category": "first_aid_survival",
        "sub_category": "Vật dụng và bảo hộ chằng chống nhà",
        "difficulty": "easy",
        "question": "Để chằng chống nhà cửa an toàn, hộ gia đình cần chuẩn bị những vật dụng và dụng cụ bảo hộ cá nhân nào?",
        "ground_truth_context": "## 3. Các dụng cụ cần thiết để chằn chống nhà cửa:\n- Tre, hoặc các loại cây khác có thể thay thế tre. 10-12 cây.\n- Bao đựng cát (đất) từ 12 đến 20 cái.\n- Thang 02 cái.\n- Kìm, búa, rựa, xên, cuốc,...\n- Đinh 5 phân, 10 phân,... dây thép (dây mây, dây ni lông, dây dừa,..)\n- Cọc để làm neo\n\n## 4. Các dụng cụ bảo hộ cá nhân cần thiết:\n- Mũ bảo hộ.\n- Găng tay vải.\n- Bộ đồ mưa",
        "ground_truth_answer": "Dụng cụ cần thiết gồm: 10-12 cây tre (hoặc cây thay thế), 12-20 bao cát/đất, 02 cái thang, kìm, búa, rựa, xẻng, cuốc, đinh 5-10 phân, dây buộc (dây thép/dây mây/dây nilông) và cọc neo. Dụng cụ bảo hộ gồm: mũ bảo hộ, găng tay vải và bộ đồ đi mưa.",
        "keywords": ["dụng cụ", "chằng chống nhà", "bao cát", "cây tre", "dây thép", "mũ bảo hộ", "găng tay"]
    },
    {
        "id": "TERRA_QA_008",
        "source_document": "0575f59d64e3407fa40049196cd01c5d.md",
        "category": "first_aid_survival",
        "sub_category": "Sơ cứu vết thương chảy máu không có dị vật",
        "difficulty": "medium",
        "question": "Khi nạn nhân bị thương chảy máu nhiều nhưng không có dị vật, quy trình sơ cứu cầm máu gồm các bước nào?",
        "ground_truth_context": "### a. Vết thương chảy máu nhiều không có dị vật:\n\n*   Không tiếp xúc trực tiếp với máu bằng cách đeo găng tay cao su, ni lon và vật dụng thay thế\n\n> [MÔ TẢ HÌNH ẢNH]: Hình ảnh cận cảnh một bàn tay đang được băng bó bằng băng gạc màu trắng. Một bàn tay khác đeo găng tay màu xanh đang giữ chặt băng.\n\n*   Dùng gạc, vải sạch, ép trực tiếp lên vết thương và giữ chặt để cầm máu.\n\n> [MÔ TẢ HÌNH ẢNH]: Hình ảnh cận cảnh hai bàn tay đang giữ chặt một bàn tay khác. Một bàn tay đeo găng tay y tế màu trắng, bàn tay còn lại không đeo găng. Có vẻ như đang kiểm tra hoặc giữ vết thương.\n\n*   Băng ép trực tiếp tại vết thương\n*   Kê cao chân, ủ ấm để phòng choáng\n*   Đỡ nạn nhân nằm để làm giảm lượng máu chảy đến các vết thương.\n\n> [MÔ TẢ HÌNH ẢNH]: Hình ảnh cận cảnh một cánh tay đang được băng bó bằng băng gạc màu trắng. Hai bàn tay khác đang hỗ trợ việc băng bó.\n\n*   Kiểm tra đầu chi sau khi băng.\n*   Nếu máu vẫn chảy thấm qua băng thì băng chồng lên bằng băng khác.",
        "ground_truth_answer": "Quy trình sơ cứu gồm: (1) Đeo găng tay để tránh tiếp xúc trực tiếp với máu; (2) Dùng gạc hoặc vải sạch ép trực tiếp lên vết thương và giữ chặt; (3) Băng ép trực tiếp tại vết thương; (4) Đỡ nạn nhân nằm, kê cao chân và ủ ấm để chống choáng; (5) Kiểm tra đầu chi sau băng; (6) Nếu máu vẫn thấm qua thì băng đè lớp băng mới lên trên, không tháo lớp băng cũ.",
        "keywords": ["sơ cứu", "chảy máu", "không dị vật", "băng ép", "kê cao chân", "chống choáng", "gạc sạch"]
    },
    {
        "id": "TERRA_QA_009",
        "source_document": "0575f59d64e3407fa40049196cd01c5d.md",
        "category": "first_aid_survival",
        "sub_category": "Sơ cứu vết thương chảy máu có dị vật",
        "difficulty": "medium",
        "question": "Đối với vết thương chảy máu nhiều và có dị vật găm vào cơ thể, điều tối kỵ là gì và phải xử trí như thế nào?",
        "ground_truth_context": "### b. Khi vết thương chảy máu nhiều có dị vật:\n\n*   Không rút dị vật\n*   Mang găng tay\n*   Ép chặt mép vết thương\n*   Chèn băng, gạc quanh dị vật và băng cố định (không băng trùm qua dị vật)\n*   Nhanh chóng chuyển nạn nhân tới cơ sở y tế gần nhất.",
        "ground_truth_answer": "Điều tối kỵ tuyệt đối là KHÔNG ĐƯỢC RÚT DỊ VẬT ra. Các bước xử trí: (1) Mang găng tay bảo hộ; (2) Ép chặt hai mép vết thương xung quanh dị vật; (3) Chèn cuộn gạc/vải chèn xung quanh chân dị vật và băng cố định để giữ dị vật đứng yên (tuyệt đối không băng trùm đè lên dị vật); (4) Nhanh chóng vận chuyển nạn nhân đến cơ sở y tế gần nhất.",
        "keywords": ["sơ cứu", "dị vật", "không rút dị vật", "chèn băng gạc", "chuyển cơ sở y tế"]
    },
    {
        "id": "TERRA_QA_010",
        "source_document": "0575f59d64e3407fa40049196cd01c5d.md",
        "category": "first_aid_survival",
        "sub_category": "Dấu hiệu nhận biết gãy xương kín và hở",
        "difficulty": "medium",
        "question": "Dấu hiệu nhận biết gãy xương kín và gãy xương hở khác nhau như thế nào và đâu là nguy cơ lớn nhất?",
        "ground_truth_context": "### 1. Gãy xương kín:\nlà gãy xương mà ổ gãy không thông với bên ngoài\n*   Đau tại vùng tổn thương, đau nhói tại điểm gãy, đau tăng lên khi nạn nhân cử động.\n*   Biến dạng khác bình thường: Gồ lên, ngắn, vẹo, lệch trục, gập góc\n*   Hạn chế hoặc mất vận động, có thể có cử động bất thường.\n*   Vùng tổn thương bầm tím, sưng nề.",
        "ground_truth_answer": "Gãy xương kín là ổ gãy không thông với bên ngoài, có dấu hiệu: đau nhói điểm gãy tăng khi cử động, biến dạng lệch trục, sưng nề bầm tím, mất vận động. Gãy xương hở có ổ gãy thông ra ngoài kèm rách da, chảy máu và đầu xương có thể trồi ra ngoài. Nguy cơ lớn: đầu xương di lệch làm đứt mạch máu/thần kinh, gây choáng ngất do đau và mất máu, và nguy cơ nhiễm trùng rất cao ở gãy xương hở.",
        "keywords": ["gãy xương kín", "gãy xương hở", "ổ gãy", "biến dạng lệch trục", "rách da", "nhiễm trùng", "choáng ngất"]
    },
    {
        "id": "TERRA_QA_011",
        "source_document": "0575f59d64e3407fa40049196cd01c5d.md",
        "category": "first_aid_survival",
        "sub_category": "Nguyên tắc xử trí cố định gãy xương",
        "difficulty": "medium",
        "question": "Bốn nguyên tắc căn bản khi xử trí sơ cứu ban đầu đối với nạn nhân bị gãy xương là gì?",
        "ground_truth_context": "# I. Nguyên tắc xử trí gãy xương:\n- Giữ nguyên tình trạng ổ gãy, không kéo, nắn, lắc xương gãy\n- Đảm bảo bất động thật chắc khớp trên và khớp dưới ổ gãy\n- Trường hợp gãy xương kèm tổn thương phần mềm, tổn thương mạch máu cần sơ cứu chảy máu và vết thương phần mềm trước khi cố định xương gãy\n- Trường hợp gãy xương hở thì biến hở thành kín rồi cố định như gãy xương kín",
        "ground_truth_answer": "4 nguyên tắc xử trí gãy xương: (1) Giữ nguyên hiện trạng ổ gãy, tuyệt đối không kéo nắn, lắc xương gãy; (2) Đảm bảo bất động thật chắc khớp trên và khớp dưới của ổ gãy; (3) Nếu có tổn thương phần mềm hoặc chảy máu mạch máu, phải sơ cứu cầm máu trước khi nẹp cố định; (4) Đối với gãy hở thì băng kín để biến hở thành kín rồi cố định như gãy kín.",
        "keywords": ["nguyên tắc xử trí", "gãy xương", "không kéo nắn", "bất động 2 khớp", "cầm máu trước", "biến hở thành kín"]
    },
    {
        "id": "TERRA_QA_012",
        "source_document": "0575f59d64e3407fa40049196cd01c5d.md",
        "category": "first_aid_survival",
        "sub_category": "Sơ cứu gãy xương cẳng tay",
        "difficulty": "hard",
        "question": "Quy trình chuẩn bị và tiến hành cố định gãy xương cẳng tay bằng nẹp và băng tam giác gồm những bước nào?",
        "ground_truth_context": "## 1. Gãy xương cẳng tay:\n### a. Chuẩn bị:\n- 2 nẹp, chiều dài nẹp từ quá khớp khuỷu đến hết lòng bàn tay,\n- 4 dây,\n- 2 băng tam giác,\n- Bông, vải,\n\n### b. Tiến hành:\n- Nạn nhân ngồi (tư thế thuận lợi nhất)\n- Yêu cầu nạn nhân đỡ tay gãy\n- Đặt 2 nẹp vào cẳng tay và đệm lót\n- Buộc dây cố định nẹp ở vị trí: trên ổ gãy, dưới ổ gãy, 2 dây ở 2 đầu nẹp\n- Dùng 2 băng tam giác: treo cẳng tay và cố định cánh tay vào thân người nạn nhân",
        "ground_truth_answer": "Chuẩn bị: 2 nẹp (dài từ quá khuỷu tay đến hết lòng bàn tay), 4 dây buộc, 2 băng tam giác và bông/vải đệm lót. Tiến hành: Cho nạn nhân ngồi đỡ tay gãy; đặt 2 nẹp vào mặt trước và sau cẳng tay có đệm lót; buộc 4 dây cố định (trên ổ gãy, dưới ổ gãy, và 2 đầu nẹp); dùng 2 băng tam giác để treo cẳng tay vuông góc trước ngực và cố định cánh tay ép sát vào thân người.",
        "keywords": ["gãy xương cẳng tay", "sơ cứu", "2 nẹp", "4 dây", "2 băng tam giác", "bất động khuỷu tay"]
    }
]
