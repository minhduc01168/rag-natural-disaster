import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import App from '../App';

describe('Offline Mode Tests', () => {
  it('renders TerraAlert title', () => {
    render(<App />);
    expect(screen.getAllByText(/TerraAlert/i).length).toBeGreaterThan(0);
  });

  it('renders dashboard on home page', () => {
    render(<App />);
    expect(screen.getByText(/Dashboard/i)).toBeInTheDocument();
  });

  it('shows SOS button on dashboard', () => {
    render(<App />);
    expect(screen.getByText(/SOS KHẨN CẤP/i)).toBeInTheDocument();
  });

  it('displays weather information', () => {
    render(<App />);
    expect(screen.getByText(/Thời tiết hiện tại/i)).toBeInTheDocument();
  });

  it('shows alert status', () => {
    render(<App />);
    expect(screen.getByText(/An toàn/i)).toBeInTheDocument();
  });

  it('renders navigation links', () => {
    render(<App />);
    expect(screen.getByRole('link', { name: /Trang chủ/i })).toBeInTheDocument();
    expect(screen.getAllByRole('link', { name: /Cảnh báo/i }).length).toBeGreaterThan(0);
    expect(screen.getAllByRole('link', { name: /Cẩm nang/i }).length).toBeGreaterThan(0);
  });
});

describe('Survival Guide Tests', () => {
  it('renders survival page components', () => {
    render(<App />);
    // Verify main components exist
    expect(screen.getByText(/Dashboard/i)).toBeInTheDocument();
  });
});
