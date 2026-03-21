// GEE Failover Logic
function getFailoverMap() {
  var aoi = ee.Geometry.Point([77.1025, 28.7041]).buffer(10000).bounds();

  // 1. Try Landsat 9
  var landsat = ee.ImageCollection("LANDSAT/LC09/C02/T1_L2")
    .filterBounds(aoi)
    .filterDate('2025-06-01', '2025-12-31')
    .sort('CLOUD_COVER')
    .first();

  // 2. Try Sentinel-2
  var sentinel = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(aoi)
    .filterDate('2025-06-01', '2025-12-31')
    .sort('CLOUDY_PIXEL_PERCENTAGE')
    .first();

  // 3. Failover Logic: If Landsat clouds > 15%, use Sentinel
  var cloudScore = ee.Number(landsat.get('CLOUD_COVER'));
  var finalImage = ee.Image(ee.Algorithms.If(cloudScore.lt(15), landsat, sentinel));

  // 4. Calculate NDVI
  // Note: Landsat 9 NIR is B5, Sentinel-2 NIR is B8
  var nir = ee.String(ee.Algorithms.If(cloudScore.lt(15), 'B5', 'B8'));
  var red = ee.String(ee.Algorithms.If(cloudScore.lt(15), 'B4', 'B4'));
  
  var ndvi = finalImage.normalizedDifference([nir, red]).rename('NDVI');

  // 5. Get Map Tile URL
  var mapId = ndvi.getMap({min: 0, max: 1, palette: ['red', 'yellow', 'green']});
  return mapId.urlFormat;
}