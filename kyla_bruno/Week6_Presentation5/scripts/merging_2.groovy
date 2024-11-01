import qupath.lib.roi.GeometryTools
import qupath.lib.roi.interfaces.ROI
import org.locationtech.jts.geom.Geometry

// Function to merge two annotations
def mergeAnnotations(def annotation1, def annotation2) {
    def roi1 = annotation1.getROI()
    def roi2 = annotation2.getROI()
    
    // Convert ROIs to JTS Geometries for merging
    Geometry geom1 = GeometryTools.geometryFromROI(roi1)
    Geometry geom2 = GeometryTools.geometryFromROI(roi2)
    
    // Perform the union operation on the geometries
    Geometry mergedGeometry = geom1.union(geom2)
    
    // Convert back to an ROI
    def mergedROI = GeometryTools.roiFromGeometry(mergedGeometry, roi1.getImagePlane())
    
    // Create the merged annotation
    def mergedAnnotation = PathObjects.createAnnotationObject(mergedROI, annotation1.getPathClass())
    return mergedAnnotation
}
