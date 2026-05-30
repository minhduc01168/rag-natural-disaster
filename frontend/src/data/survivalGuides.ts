export interface SurvivalGuide {
  id: string;
  category: string;
  title: string;
  icon: string;
  description: string;
  content: string[];
}

export const categories = [
  {
    id: 'first-aid',
    name: 'Sơ cấp cứu',
    icon: '🏥',
    description: 'Kiến thức sơ cấp cứu cơ bản',
  },
  {
    id: 'natural-disasters',
    name: 'Thiên tai',
    icon: '🌊',
    description: 'Xử lý khi gặp thiên tai',
  },
  {
    id: 'emergency-contacts',
    name: 'Liên hệ khẩn cấp',
    icon: '📞',
    description: 'Số điện thoại cứu thương',
  },
  {
    id: 'survival-skills',
    name: 'Kỹ năng sinh tồn',
    icon: '🏕️',
    description: 'Kỹ năng sống sót trong tự nhiên',
  },
  {
    id: 'food-water',
    name: 'Thức ăn & Nước',
    icon: '💧',
    description: 'Tìm kiếm thức ăn và nước sạch',
  },
  {
    id: 'shelter',
    name: 'Nơi trú ẩn',
    icon: '⛺',
    description: 'Xây dựng nơi trú ẩn tạm thời',
  },
];

export const survivalGuides: SurvivalGuide[] = [
  {
    id: 'cpr',
    category: 'first-aid',
    title: 'Hồi sức tim phổi (CPR)',
    icon: '❤️',
    description: 'Kỹ thuật CPR cơ bản',
    content: [
      '1. Kiểm tra an toàn xung quanh',
      '2. Gọi cấp cứu 115',
      '3. Đặt nạn nhân nằm ngửa trên bề mặt cứng',
      '4. Đặt hai tay lên ngực, giữa hai núm vú',
      '5. Ép ngực 30 lần (sâu 5-6cm)',
      '6. Thổi ngạt 2 lần',
      '7. Lặp lại cho đến khi cứu thương đến',
    ],
  },
  {
    id: 'bleeding',
    category: 'first-aid',
    title: 'Cầm máu',
    icon: '🩸',
    description: 'Xử lý khi bị chảy máu nhiều',
    content: [
      '1. Đặt nạn nhân nằm xuống',
      '2. Dùng vải sạch ấn mạnh vào vết thương',
      '3. Giữ nguyên áp lực ít nhất 15 phút',
      '4. Nếu máu thấm qua, đặt thêm vải bên trên',
      '5. Không tháo vải cũ ra',
      '6. Gọi cấp cứu nếu máu không ngừng',
    ],
  },
  {
    id: 'flood',
    category: 'natural-disasters',
    title: 'Xử lý khi lũ lụt',
    icon: '🌊',
    description: 'An toàn khi gặp lũ lụt',
    content: [
      '1. Di chuyển đến nơi cao ngay lập tức',
      '2. Không đi qua vùng nước chảy xiết',
      '3. Nếu bị kẹt, lên tầng cao nhất',
      '4. Chuẩn bị đồ cấp cứu và nước uống',
      '5. Tắt điện và gas để tránh cháy nổ',
      '6. Liên hệ cứu hộ nếu cần thiết',
      '7. Không quay về nhà cho đến khi an toàn',
    ],
  },
  {
    id: 'landslide',
    category: 'natural-disasters',
    title: 'Xử lý khi sạt lở đất',
    icon: '⛰️',
    description: 'An toàn khi gặp sạt lở',
    content: [
      '1. Di chuyển ra xa khu vực sạt lở',
      '2. Không ở dưới chân đồi hoặc núi',
      '3. Nghe tiếng động bất thường → chạy ngay',
      '4. Tìm nơi đất cứng, ổn định',
      '5. Nếu bị kẹt, bảo vệ đầu và hô hấp',
      '6. Gọi cứu hộ 113 hoặc 115',
    ],
  },
  {
    id: 'emergency-numbers',
    category: 'emergency-contacts',
    title: 'Số điện thoại khẩn cấp',
    icon: '📱',
    description: 'Các số điện thoại cần nhớ',
    content: [
      '🚨 Cấp cứu: 115',
      '🚒 Cứu hỏa: 114',
      '👮 Cảnh sát: 113',
      '🚑 Cứu thương: 115',
      '📞 Tổng đài khẩn cấp: 112',
      '🌊 Cứu hộ thiên tai: 1900 1567',
    ],
  },
  {
    id: 'find-water',
    category: 'survival-skills',
    title: 'Tìm nước sạch',
    icon: '💧',
    description: 'Cách tìm và lọc nước',
    content: [
      '1. Tìm nguồn nước chảy (suối, sông)',
      '2. Thu nước mưa bằng vải sạch',
      '3. Đun sôi nước ít nhất 1 phút',
      '4. Nếu không đun được, dùng vải lọc',
      '5. Nước từ cây: buộc túi nilon vào cành',
      '6. Tránh nước đọng, nước có màu lạ',
    ],
  },
  {
    id: 'build-shelter',
    category: 'shelter',
    title: 'Xây dựng nơi trú ẩn',
    icon: '⛺',
    description: 'Cách xây dựng lều tạm',
    content: [
      '1. Chọn nơi khô ráo, bằng phẳng',
      '2. Tránh nơi có nguy cơ sạt lở',
      '3. Dùng cành cây làm khung',
      '4. Che phủ bằng lá, vải hoặc bạt',
      '5. Đảm bảo thoát nước mưa',
      '6. Cách mặt đất ít nhất 10cm',
    ],
  },
  {
    id: 'find-food',
    category: 'food-water',
    title: 'Tìm kiếm thức ăn',
    icon: '🍎',
    description: 'Cách tìm thức ăn trong tự nhiên',
    content: [
      '1. Ưu tiên tìm quả chín (dâu, chuối)',
      '2. Kiểm tra côn trùng ăn được (dế, châu chấu)',
      '3. Tránh nấm màu sặc sỡ',
      '4. Cá và tôm là nguồn protein tốt',
      '5. Rau dại: thử một ít trước khi ăn nhiều',
      '6. Nếu không chắc → không ăn',
    ],
  },
];

export function getGuidesByCategory(categoryId: string): SurvivalGuide[] {
  return survivalGuides.filter((guide) => guide.category === categoryId);
}

export function searchGuides(query: string): SurvivalGuide[] {
  const lowerQuery = query.toLowerCase();
  return survivalGuides.filter(
    (guide) =>
      guide.title.toLowerCase().includes(lowerQuery) ||
      guide.description.toLowerCase().includes(lowerQuery)
  );
}
