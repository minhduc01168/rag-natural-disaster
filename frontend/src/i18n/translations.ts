export type Language = 'vi' | 'en';

export type TranslationKeys = {
  nav: {
    home: string;
    alerts: string;
    survival: string;
    research: string;
    admin: string;
    login: string;
    register: string;
    logout: string;
    hello: string;
  };
  common: {
    refresh: string;
    loading: string;
    error: string;
    success: string;
    cancel: string;
    delete: string;
    confirmDelete: string;
    close: string;
    save: string;
    retry: string;
    offlineTitle: string;
    offlineDesc: string;
    footerText: string;
  };
  home: {
    title: string;
    subtitle: string;
    activeAlerts: string;
    weatherStation: string;
    safetyIndex: string;
    quickActions: string;
    emergencyCall: string;
    reportIncident: string;
    evacuationMap: string;
    aiAssistant: string;
  };
  weather: {
    title: string;
    currentTemp: string;
    humidity: string;
    windSpeed: string;
    pressure: string;
    uvIndex: string;
    rainfall: string;
    lastUpdated: string;
    refreshData: string;
    statusNormal: string;
    statusWarning: string;
    statusDanger: string;
    statusLabel: string;
    location: string;
  };
  alerts: {
    title: string;
    subtitle: string;
    filterAll: string;
    filterEmergency: string;
    filterWarning: string;
    filterAdvisory: string;
    riskHigh: string;
    riskMedium: string;
    riskLow: string;
    viewDetails: string;
    locationLabel: string;
    timeLabel: string;
    sourceLabel: string;
    emptyTitle: string;
    emptyDesc: string;
    showing: string;
  };
  survival: {
    title: string;
    subtitle: string;
    cpr: string;
    flood: string;
    earthquake: string;
    fire: string;
    water: string;
    firstAid: string;
    step: string;
    warningNote: string;
    emergencyContacts: string;
    callNow: string;
    searchPlaceholder: string;
    searchResults: string;
    noResults: string;
    backToCat: string;
    back: string;
    guideLabel: string;
    offlineNotice: string;
  };
  research: {
    title: string;
    subtitle: string;
    tabTrends: string;
    tabModels: string;
    tabReports: string;
    exportData: string;
    filterRegion: string;
    chartTitle: string;
    layerLsm: string;
    layerDisaster: string;
    layerElevation: string;
    statsTitle: string;
    totalPoints: string;
    dataLayer: string;
    riskDist: string;
  };
  bot: {
    title: string;
    subtitle: string;
    placeholder: string;
    send: string;
    welcome: string;
    errorMsg: string;
    replyWeather: string;
    replyCpr: string;
    replyFlood: string;
    replyWater: string;
    quickWeather: string;
    quickCpr: string;
    quickFlood: string;
    quickWater: string;
    openBot: string;
    closeBot: string;
    tooltipExpand: string;
    tooltipCompress: string;
    tooltipClose: string;
    expandTooltip: string;
    collapseTooltip: string;
    closeTooltip: string;
  };
  admin: {
    controlRoom: string;
    title: string;
    subtitle: string;
    navUpload: string;
    navDocs: string;
    navManage: string;
    kbTitle: string;
    kbSubtitle: string;
    uploadBtn: string;
    step1: string;
    step1Note: string;
    dryRun: string;
    analyzing: string;
    step2: string;
    commit: string;
    committing: string;
    chunks: string;
    kbDocsTitle: string;
    kbDocsSubtitle: string;
    docsTitle: string;
    docsSubtitle: string;
    refresh: string;
    refreshBtn: string;
    delete: string;
    deleteBtn: string;
    cancel: string;
    confirmDelete: string;
    deleteConfirmQuestion: string;
    loading: string;
    statsDocs: string;
    statsChunks: string;
    statsAvg: string;
    totalDocs: string;
    totalChunks: string;
    avgChunks: string;
    viewChunks: string;
    viewingChunks: string;
    clickToView: string;
    noDocs: string;
    emptyDocs: string;
    statusLabel: string;
    statusReady: string;
    statusProcessing: string;
    statusFailed: string;
    statusReadyDesc: string;
    statusProcessingDesc: string;
  };
};

export const translations: Record<Language, TranslationKeys> = {
  vi: {
    nav: {
      home: 'Trang chủ',
      alerts: 'Cảnh báo',
      survival: 'Cẩm nang',
      research: '📊 Nghiên cứu',
      admin: '⚙️ Quản trị',
      login: 'Đăng nhập',
      register: 'Đăng ký',
      logout: 'Đăng xuất',
      hello: 'Chào',
    },
    common: {
      refresh: 'Làm mới',
      loading: 'Đang tải...',
      error: 'Có lỗi xảy ra',
      success: 'Thành công',
      cancel: 'Hủy',
      delete: 'Xóa',
      confirmDelete: 'Xác nhận xóa?',
      close: 'Đóng',
      save: 'Lưu',
      retry: 'Thử lại',
      offlineTitle: 'Không có kết nối',
      offlineDesc: 'Vui lòng kiểm tra mạng và thử lại',
      footerText: 'TerraAlert - Hệ thống Cảnh báo Thiên tai Thông minh',
    },
    home: {
      title: 'Hệ thống Cảnh báo Thiên tai Sớm',
      subtitle: 'Giám sát thời tiết, cảnh báo rủi ro và hướng dẫn an toàn theo thời gian thực',
      activeAlerts: 'Cảnh báo Đang kích hoạt',
      weatherStation: 'Trạm Quan trắc Thời tiết',
      safetyIndex: 'Chỉ số An toàn Cực đại',
      quickActions: 'Thao tác Khẩn cấp',
      emergencyCall: 'Gọi Cứu hộ (112)',
      reportIncident: 'Báo cáo Sự cố',
      evacuationMap: 'Bản đồ Sơ tán',
      aiAssistant: 'Hỏi Trợ lý AI',
    },
    weather: {
      title: 'Thời tiết hiện tại',
      currentTemp: 'Nhiệt độ',
      humidity: 'Độ ẩm',
      windSpeed: 'Tốc độ gió',
      pressure: 'Áp suất',
      uvIndex: 'Chỉ số UV',
      rainfall: 'Lượng mưa',
      lastUpdated: 'Cập nhật lúc',
      refreshData: 'Làm mới dữ liệu',
      statusNormal: 'Bình thường',
      statusWarning: 'Cảnh báo',
      statusDanger: 'Khẩn cấp',
      statusLabel: 'Tình trạng',
      location: 'Hà Nội, Việt Nam',
    },
    alerts: {
      title: 'Trung tâm Cảnh báo',
      subtitle: 'Danh sách cảnh báo thời tiết và thiên tai theo thời gian thực',
      filterAll: 'Tất cả',
      filterEmergency: 'Khẩn cấp',
      filterWarning: 'Cảnh báo',
      filterAdvisory: 'Theo dõi',
      riskHigh: 'Rủi ro Cao',
      riskMedium: 'Rủi ro Trung bình',
      riskLow: 'Rủi ro Thấp',
      viewDetails: 'Xem chi tiết',
      locationLabel: 'Khu vực:',
      timeLabel: 'Thời gian:',
      sourceLabel: 'Nguồn:',
      emptyTitle: 'Không có cảnh báo nào',
      emptyDesc: 'Hệ thống đang theo dõi thời tiết và rủi ro thiên tai...',
      showing: 'Hiển thị',
    },
    survival: {
      title: 'Cẩm nang Sinh tồn & Sơ cấp cứu',
      subtitle: 'Kiến thức thiết yếu giúp bạn và gia đình an toàn trước thiên tai - hoạt động offline',
      cpr: 'Sơ cấp cứu CPR',
      flood: 'Ứng phó Lũ lụt',
      earthquake: 'Động đất & Sạt lở',
      fire: 'An toàn Cháy nổ',
      water: 'Lọc nước sạch',
      firstAid: 'Băng bó & Cứu thương',
      step: 'Bước',
      warningNote: 'Lưu ý quan trọng',
      emergencyContacts: 'Danh bạ Khẩn cấp',
      callNow: 'Gọi ngay',
      searchPlaceholder: 'Tìm kiếm cẩm nang...',
      searchResults: 'Kết quả tìm kiếm',
      noResults: 'Không tìm thấy kết quả',
      backToCat: 'Quay lại danh mục',
      back: 'Quay lại',
      guideLabel: 'Hướng dẫn chi tiết:',
      offlineNotice: '📱 Nội dung này được lưu trữ và hoạt động offline ngay cả khi mất mạng',
    },
    research: {
      title: 'Trung tâm Nghiên cứu & Dữ liệu GIS',
      subtitle: 'Phân tích dữ liệu địa không gian và bản đồ nhạy cảm sạt lở đất (LSM)',
      tabTrends: 'Xu hướng Khí hậu',
      tabModels: 'Mô hình AI & Dự báo',
      tabReports: 'Báo cáo Định kỳ',
      exportData: 'Xuất báo cáo (CSV/PDF)',
      filterRegion: 'Lọc theo khu vực',
      chartTitle: 'Biểu đồ Tần suất Thiên tai theo Năm',
      layerLsm: '🗺️ Bản đồ LSM',
      layerDisaster: '⚠️ Thiên tai',
      layerElevation: '⛰️ Cao độ',
      statsTitle: 'Thống kê lớp dữ liệu',
      totalPoints: 'Tổng điểm dữ liệu:',
      dataLayer: 'Lớp đang chọn:',
      riskDist: 'Phân bố mức độ rủi ro',
    },
    bot: {
      title: 'TerraBot',
      subtitle: 'Trợ lý AI • Sẵn sàng hỗ trợ',
      placeholder: 'Nhập câu hỏi... (Enter để gửi)',
      send: 'Gửi',
      welcome: 'Xin chào! Tôi là TerraBot - Trợ lý AI Cảnh báo Thiên tai & Sơ cấp cứu. Tôi có thể giúp gì cho bạn hôm nay?',
      errorMsg: 'Xin lỗi, hiện tại tôi không thể kết nối tới máy chủ. Vui lòng thử lại sau hoặc gọi hotline khẩn cấp 112 nếu gặp nguy hiểm.',
      replyWeather: '🌦️ Thời tiết & Cảnh báo hôm nay',
      replyCpr: '🫀 Hướng dẫn sơ cấp cứu CPR',
      replyFlood: '🌊 Ứng phó khi ngập lụt khẩn cấp',
      replyWater: '💧 Cách lọc nước sạch sinh tồn',
      quickWeather: 'Thời tiết hôm nay',
      quickCpr: 'Sơ cấp cứu CPR',
      quickFlood: 'Xử lý lũ lụt',
      quickWater: 'Tìm nước sạch',
      openBot: 'Mở TerraBot',
      closeBot: 'Đóng TerraBot',
      tooltipExpand: 'Phóng to',
      tooltipCompress: 'Thu nhỏ',
      tooltipClose: 'Đóng',
      expandTooltip: 'Phóng to',
      collapseTooltip: 'Thu nhỏ (Esc)',
      closeTooltip: 'Đóng (Esc)',
    },
    admin: {
      controlRoom: 'Trung tâm Điều hành',
      title: 'Trung tâm Điều hành',
      subtitle: 'Bảng điều khiển Quản trị',
      navUpload: 'Tải lên Tài liệu',
      navDocs: 'Quản lý Tài liệu',
      navManage: 'Quản lý Tài liệu',
      kbTitle: 'Quản lý Tài liệu',
      kbSubtitle: 'Tải lên tài liệu mới để nạp vào hệ thống RAG',
      uploadBtn: 'Tải lên & Nạp dữ liệu',
      step1: 'Bước 1: Tải tài liệu & Phân tích',
      step1Note: 'Hệ thống sử dụng Hierarchical Chunking để bóc tách và tạo preview trước khi lưu vào cơ sở dữ liệu vector.',
      dryRun: '🔍 Phân tích thử',
      analyzing: '⏳ Đang phân tích...',
      step2: 'Bước 2: Kiểm duyệt & Nạp vào RAG',
      commit: '🚀 Duyệt & Nạp vào RAG',
      committing: '⏳ Đang lưu vào CSDL & Vector DB...',
      chunks: 'chunks',
      kbDocsTitle: 'Quản lý Tài liệu',
      kbDocsSubtitle: 'Danh sách tài liệu đã nạp vào hệ thống · Click để xem chunks',
      docsTitle: 'Quản lý Tài liệu',
      docsSubtitle: 'Danh sách tài liệu đã nạp vào hệ thống · Click để xem chi tiết chunks',
      refresh: 'Làm mới',
      refreshBtn: 'Làm mới',
      delete: 'Xóa',
      deleteBtn: 'Xóa',
      cancel: 'Hủy',
      confirmDelete: 'Xác nhận xóa?',
      deleteConfirmQuestion: 'Xác nhận xóa?',
      loading: 'Đang tải...',
      statsDocs: 'Tài liệu',
      statsChunks: 'Tổng chunks',
      statsAvg: 'TB chunks/file',
      totalDocs: 'Tổng tài liệu',
      totalChunks: 'Tổng chunks',
      avgChunks: 'TB chunks/file',
      viewChunks: 'Xem chunks →',
      viewingChunks: 'Đang xem chunks ↓',
      clickToView: 'Click để xem chunks →',
      noDocs: 'Chưa có tài liệu nào được nạp vào hệ thống.',
      emptyDocs: 'Chưa có tài liệu nào được nạp vào hệ thống.',
      statusLabel: 'Trạng thái',
      statusReady: 'Sẵn sàng',
      statusProcessing: 'Đang xử lý',
      statusFailed: 'Lỗi',
      statusReadyDesc: 'Đã nạp và lập chỉ mục trong RAG Vector DB',
      statusProcessingDesc: 'Đang bóc tách và tạo vector nhúng',
    },
  },
  en: {
    nav: {
      home: 'Home',
      alerts: 'Alerts',
      survival: 'Handbook',
      research: '📊 Research',
      admin: '⚙️ Admin',
      login: 'Login',
      register: 'Register',
      logout: 'Logout',
      hello: 'Hi',
    },
    common: {
      refresh: 'Refresh',
      loading: 'Loading...',
      error: 'An error occurred',
      success: 'Success',
      cancel: 'Cancel',
      delete: 'Delete',
      confirmDelete: 'Confirm delete?',
      close: 'Close',
      save: 'Save',
      retry: 'Retry',
      offlineTitle: 'No Connection',
      offlineDesc: 'Please check your network and try again',
      footerText: 'TerraAlert - Intelligent Disaster Warning System',
    },
    home: {
      title: 'Early Disaster Warning System',
      subtitle: 'Real-time weather monitoring, risk alerts, and emergency safety guidelines',
      activeAlerts: 'Active Alerts',
      weatherStation: 'Weather Monitoring Station',
      safetyIndex: 'Max Safety Index',
      quickActions: 'Emergency Actions',
      emergencyCall: 'Rescue Call (112)',
      reportIncident: 'Report Incident',
      evacuationMap: 'Evacuation Map',
      aiAssistant: 'Ask AI Assistant',
    },
    weather: {
      title: 'Current Weather',
      currentTemp: 'Temperature',
      humidity: 'Humidity',
      windSpeed: 'Wind Speed',
      pressure: 'Pressure',
      uvIndex: 'UV Index',
      rainfall: 'Rainfall',
      lastUpdated: 'Updated at',
      refreshData: 'Refresh Data',
      statusNormal: 'Normal',
      statusWarning: 'Warning',
      statusDanger: 'Emergency',
      statusLabel: 'Condition',
      location: 'Hanoi, Vietnam',
    },
    alerts: {
      title: 'Alert Center',
      subtitle: 'Real-time weather and natural disaster alerts list',
      filterAll: 'All',
      filterEmergency: 'Emergency',
      filterWarning: 'Warning',
      filterAdvisory: 'Advisory',
      riskHigh: 'High Risk',
      riskMedium: 'Medium Risk',
      riskLow: 'Low Risk',
      viewDetails: 'View Details',
      locationLabel: 'Location:',
      timeLabel: 'Time:',
      sourceLabel: 'Source:',
      emptyTitle: 'No active alerts',
      emptyDesc: 'System is monitoring real-time weather and disaster risks...',
      showing: 'Showing',
    },
    survival: {
      title: 'Survival & First Aid Handbook',
      subtitle: 'Essential knowledge to keep you and your family safe during disasters - offline ready',
      cpr: 'CPR First Aid',
      flood: 'Flood Response',
      earthquake: 'Earthquake & Landslide',
      fire: 'Fire Safety',
      water: 'Clean Water Filtration',
      firstAid: 'Bandaging & First Aid',
      step: 'Step',
      warningNote: 'Important Note',
      emergencyContacts: 'Emergency Contacts',
      callNow: 'Call Now',
      searchPlaceholder: 'Search handbook...',
      searchResults: 'Search results',
      noResults: 'No results found',
      backToCat: 'Back to categories',
      back: 'Back',
      guideLabel: 'Step-by-step instructions:',
      offlineNotice: '📱 This content is cached and works offline without internet connection',
    },
    research: {
      title: 'GIS Research & Data Hub',
      subtitle: 'Geospatial analysis and Landslide Susceptibility Mapping (LSM)',
      tabTrends: 'Climate Trends',
      tabModels: 'AI Models & Forecasts',
      tabReports: 'Periodic Reports',
      exportData: 'Export Report (CSV/PDF)',
      filterRegion: 'Filter by region',
      chartTitle: 'Disaster Frequency Chart by Year',
      layerLsm: '🗺️ LSM Map',
      layerDisaster: '⚠️ Disasters',
      layerElevation: '⛰️ Elevation',
      statsTitle: 'Layer Statistics',
      totalPoints: 'Total Data Points:',
      dataLayer: 'Active Layer:',
      riskDist: 'Risk Level Distribution',
    },
    bot: {
      title: 'TerraBot',
      subtitle: 'AI Assistant • Ready to assist',
      placeholder: 'Type your question... (Enter to send)',
      send: 'Send',
      welcome: 'Hello! I am TerraBot - AI Disaster Warning & First Aid Assistant. How can I help you today?',
      errorMsg: 'Sorry, I cannot connect to the server right now. Please try again later or call emergency hotline 112 if in danger.',
      replyWeather: '🌦️ Today\'s Weather & Alerts',
      replyCpr: '🫀 CPR First Aid Guide',
      replyFlood: '🌊 Emergency Flood Response',
      replyWater: '💧 Clean Water Filtration Guide',
      quickWeather: 'Today weather',
      quickCpr: 'CPR first aid',
      quickFlood: 'Flood response',
      quickWater: 'Find clean water',
      openBot: 'Open TerraBot',
      closeBot: 'Close TerraBot',
      tooltipExpand: 'Expand',
      tooltipCompress: 'Compress',
      tooltipClose: 'Close',
      expandTooltip: 'Expand',
      collapseTooltip: 'Compress (Esc)',
      closeTooltip: 'Close (Esc)',
    },
    admin: {
      controlRoom: 'Control Room',
      title: 'Control Room',
      subtitle: 'Admin Dashboard',
      navUpload: 'Upload Documents',
      navDocs: 'Document Management',
      navManage: 'Document Management',
      kbTitle: 'Document Management',
      kbSubtitle: 'Upload new documents to ingest into the RAG system',
      uploadBtn: 'Upload & Ingest',
      step1: 'Step 1: Upload & Analyze',
      step1Note: 'System uses Hierarchical Chunking to extract and create preview before saving to vector database.',
      dryRun: '🔍 Preliminary Analysis',
      analyzing: '⏳ Analyzing...',
      step2: 'Step 2: Review & Ingest into RAG',
      commit: '🚀 Approve & Ingest into RAG',
      committing: '⏳ Saving to DB & Vector DB...',
      chunks: 'chunks',
      kbDocsTitle: 'Document Management',
      kbDocsSubtitle: 'List of documents ingested into system · Click to inspect chunks',
      docsTitle: 'Document Management',
      docsSubtitle: 'List of documents ingested into system · Click to view chunk details',
      refresh: 'Refresh',
      refreshBtn: 'Refresh',
      delete: 'Delete',
      deleteBtn: 'Delete',
      cancel: 'Cancel',
      confirmDelete: 'Confirm delete?',
      deleteConfirmQuestion: 'Confirm delete?',
      loading: 'Loading...',
      statsDocs: 'Documents',
      statsChunks: 'Total Chunks',
      statsAvg: 'Avg Chunks/File',
      totalDocs: 'Total Documents',
      totalChunks: 'Total Chunks',
      avgChunks: 'Avg Chunks/File',
      viewChunks: 'View chunks →',
      viewingChunks: 'Viewing chunks ↓',
      clickToView: 'Click to view chunks →',
      noDocs: 'No documents ingested into system yet.',
      emptyDocs: 'No documents ingested into system yet.',
      statusLabel: 'Status',
      statusReady: 'Ready',
      statusProcessing: 'Processing',
      statusFailed: 'Failed',
      statusReadyDesc: 'Ingested and indexed in RAG Vector DB',
      statusProcessingDesc: 'Extracting and generating embeddings',
    },
  },
};
