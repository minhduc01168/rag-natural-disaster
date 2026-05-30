import { ChatWindow } from '../components/chat/ChatWindow';

export function TerraBotPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">TerraBot Space</h2>
        <p className="text-gray-600 mt-1">
          Trợ lý AI hỗ trợ phòng chống thiên tai và sinh tồn
        </p>
      </div>

      <div className="max-w-2xl mx-auto">
        <ChatWindow />
      </div>

      <div className="text-center text-sm text-gray-400 pt-4">
        <p>TerraBot sử dụng AI để trả lời câu hỏi về thiên tai và sinh tồn</p>
        <p className="mt-1">Lưu ý: Thông tin chỉ mang tính tham khảo</p>
      </div>
    </div>
  );
}
