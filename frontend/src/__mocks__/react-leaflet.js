const React = require('react');

const MapContainer = ({ children, ...props }) => React.createElement('div', { 'data-testid': 'map-container', ...props }, children);
const TileLayer = () => React.createElement('div', { 'data-testid': 'tile-layer' });
const GeoJSON = () => React.createElement('div', { 'data-testid': 'geojson' });
const Marker = ({ children }) => React.createElement('div', { 'data-testid': 'marker' }, children);
const Popup = ({ children }) => React.createElement('div', { 'data-testid': 'popup' }, children);

module.exports = {
  MapContainer,
  TileLayer,
  GeoJSON,
  Marker,
  Popup,
  useMap: () => ({ setView: jest.fn() }),
  useMapEvent: () => null,
  useMapEvents: () => null,
};
