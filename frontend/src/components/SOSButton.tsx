import { useState } from 'react';

interface SOSButtonProps {
  onSOS?: () => void;
}

export function SOSButton({ onSOS }: SOSButtonProps) {
  const [isPressed, setIsPressed] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const handlePress = () => {
    setIsPressed(true);
    setShowConfirm(true);
    setTimeout(() => setIsPressed(false), 200);
  };

  const handleConfirm = () => {
    setShowConfirm(false);
    if (onSOS) {
      onSOS();
    }
    // In real app, this would send SOS to backend
    alert('Tín hiệu SOS đã được gửi! Đội cứu nạn sẽ liên hệ sớm.');
  };

  const handleCancel = () => {
    setShowConfirm(false);
  };

  return (
    <>
      <button
        onClick={handlePress}
        className={`w-full py-6 bg-red-600 hover:bg-red-700 text-white rounded-xl shadow-lg transition-all transform ${
          isPressed ? 'scale-95' : 'scale-100'
        } active:scale-95`}
      >
        <div className="flex items-center justify-center gap-3">
          <span className="text-3xl">🚨</span>
          <div>
            <p className="text-xl font-bold">SOS KHẨN CẤP</p>
            <p className="text-sm opacity-90">Nhấn để gửi tín hiệu cứu nạn</p>
          </div>
        </div>
      </button>

      {showConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 max-w-sm mx-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Xác nhận gửi SOS?</h3>
            <p className="text-gray-600 mb-4">
              Tín hiệu SOS sẽ được gửi đến đội cứu nạn. Họ sẽ liên hệ với bạn trong thời gian sớm nhất.
            </p>
            <div className="flex gap-3">
              <button
                onClick={handleCancel}
                className="flex-1 py-2 px-4 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                Hủy
              </button>
              <button
                onClick={handleConfirm}
                className="flex-1 py-2 px-4 bg-red-600 text-white rounded-lg hover:bg-red-700"
              >
                Gửi SOS
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
