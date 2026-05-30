import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App', () => {
  it('renders TerraAlert title', () => {
    render(<App />);
    const titleElements = screen.getAllByText(/TerraAlert/i);
    expect(titleElements.length).toBeGreaterThan(0);
  });

  it('renders Dashboard heading', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { name: /Dashboard/i });
    expect(heading).toBeInTheDocument();
  });

  it('renders navigation links', () => {
    render(<App />);
    expect(screen.getByRole('link', { name: /Trang chủ/i })).toBeInTheDocument();
    expect(screen.getAllByRole('link', { name: /Cảnh báo/i }).length).toBeGreaterThan(0);
    expect(screen.getAllByRole('link', { name: /Cẩm nang/i }).length).toBeGreaterThan(0);
  });

  it('renders SOS button', () => {
    render(<App />);
    expect(screen.getByText(/SOS KHẨN CẤP/i)).toBeInTheDocument();
  });

  it('renders weather card', () => {
    render(<App />);
    expect(screen.getByText(/Thời tiết hiện tại/i)).toBeInTheDocument();
    expect(screen.getByText(/Nhiệt độ/i)).toBeInTheDocument();
    expect(screen.getByText(/Độ ẩm/i)).toBeInTheDocument();
  });

  it('renders alert status', () => {
    render(<App />);
    expect(screen.getByText(/An toàn/i)).toBeInTheDocument();
  });
});
