// RUN FOR PROJECT

// load libraries
import qupath.lib.objects.PathObjects
import qupath.lib.roi.RoiTools
import qupath.lib.roi.GeometryTools
import qupath.lib.roi.interfaces.ROI
import org.locationtech.jts.geom.Geometry


// CREATE ANNOTATIONS ================================
def applyClassifier(project, imageName) {
    def projectBaseDir = project.getBaseDirectory()
    
    // Retrieve the pixel size (µm/pixel)
    double pixelSize = getCurrentImageData().getServer().getPixelCalibration().getAveragedPixelSizeMicrons()
    double pixelSizeSq = Math.pow(pixelSize, 2) // Convert to µm²/pixel² for area conversion
    
    // Annotation Params
    // Convert from µm² to pixels²
    double minArea = 0 / pixelSizeSq
    double minHoleArea = 1e8 / pixelSizeSq
    
    // Identify the correct pixel classifier using filename
    if (imageName.toLowerCase().contains("h&e")) {
        // load correct classifier
        def heClassifier = new File(projectBaseDir, "classifiers/pixel_classifiers/find_tissue_h&e.json").getAbsolutePath()
        print("Applying H&E classifier to " + imageName)
        
        // Clear any existing objects (so dont have to reload)
        clearAllObjects()
        
        // Create Objects
        createAnnotationsFromPixelClassifier(heClassifier, minArea, minHoleArea)
       
        
    } else if (imageName.toLowerCase().contains("mela")) {
        
        def melanClassifier = new File(projectBaseDir, "classifiers/pixel_classifiers/find_tissue_melan.json").getAbsolutePath()
        print("Applying Melan classifier to " + imageName)
        clearAllObjects()
        createAnnotationsFromPixelClassifier(melanClassifier, minArea, minHoleArea)
        
        def annotations1 = getAnnotationObjects()
    
        print "Number of tissue annotations found by classifier: ${annotations1.size()}"
       
    } else if (imageName.toLowerCase().contains("sox10")) {
        
        def sox10Classifier = new File(projectBaseDir, "classifiers/pixel_classifiers/find_tissue_sox10.json").getAbsolutePath()
        print("Applying Sox10 classifier to " + imageName)
        clearAllObjects()
        createAnnotationsFromPixelClassifier(sox10Classifier, minArea, minHoleArea)
    } else {
        print "Could not find stain type from image file's name"
        return
    }
    
}
      

// SPLIT ANNOTATIONS INTO SEPARATE TISSUES =====================================
def splitAnnotations() {
    // Get all annotations made in the current image
    def annotations = getAnnotationObjects()
    
    // Define the desired class (create it if it doesn't already exist)
    def tissueClass = getPathClass("Tissue")
    
    // for each annotation (usually just one big one)
    annotations.each { annotation ->

        // Split the annotation by identifying the individual parts
        def roi = annotation.getROI()
        def splitROIs = RoiTools.splitROI(roi)
    
        // Create separate annotation objects for each one
        splitROIs.each { subROI ->
            def subAnnotation = PathObjects.createAnnotationObject(subROI)
            addObject(subAnnotation)
            // set class to Tissue
            subAnnotation.setPathClass(tissueClass)
         }
    
         // Remove the original annotation
         removeObject(annotation, true)
    }

// Update the hierarchy (just in case)
// unsure where this would go
fireHierarchyUpdate()
}



// MERGE BROKEN TISSUE SEGMENTS =============================

// Calculate Euclidean distance between two annotations in micrometers
double calculateDistanceCentroid(def annotation1, def annotation2, double pixelSize) {
    double x1 = annotation1.getROI().getCentroidX()
    double y1 = annotation1.getROI().getCentroidY()
    double x2 = annotation2.getROI().getCentroidX()
    double y2 = annotation2.getROI().getCentroidY()

    // Calculate distance in pixels and convert to micrometers
    double pixelDistance = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2))
    return pixelDistance * pixelSize
}




// helper function to perform merge on two selected annotations
def mergeTwoAnnotations(def annotation1, def annotation2) {
    def roi1 = annotation1.getROI()
    def roi2 = annotation2.getROI()
    
    // Convert ROIs to JTS Geometries for merging
    Geometry geom1 = GeometryTools.roiToGeometry(roi1)
    Geometry geom2 = GeometryTools.roiToGeometry(roi2)
    
    // Union operation
    Geometry mergedGeometry = geom1.union(geom2)
    
    // Convert back to ROI
    def mergedROI = GeometryTools.geometryToROI(mergedGeometry, roi1.getImagePlane())
    
    // Create merged annotation
    def mergedAnnotation = PathObjects.createAnnotationObject(mergedROI, annotation1.getPathClass())
    return mergedAnnotation
}


// Merge annotations within a threshold distance (in micrometers)
def mergeAnnotations(double micrometerThreshold = 200.0) {
    def tissueAnnotations = getAnnotationObjects().findAll { 
        it.getPathClass() != null && it.getPathClass().getName() == "Tissue" 
    }
    
    // Get the pixel size in micrometers
    def pixelSize = getCurrentImageData().getServer().getPixelCalibration().getAveragedPixelSizeMicrons()
    if (pixelSize <= 0) {
        throw new IllegalStateException("Pixel size must be greater than zero")
    }

    // Convert micrometer threshold to pixel distance
    double pixelThreshold = micrometerThreshold / pixelSize

    boolean merged
    do {
        merged = false
        def toRemove = []
        def toAdd = []

        for (int i = 0; i < tissueAnnotations.size(); i++) {
            def annotation1 = tissueAnnotations[i]

            for (int j = i + 1; j < tissueAnnotations.size(); j++) {
                def annotation2 = tissueAnnotations[j]

                // Calculate distance in pixels
                double distance = calculateDistanceCentroid(annotation1, annotation2, pixelSize)

                // Compare using the pixel threshold
                if (distance < pixelThreshold) {
                    def mergedAnnotation = mergeTwoAnnotations(annotation1, annotation2)

                    if (mergedAnnotation != null) {
                        toRemove.add(annotation1)
                        toRemove.add(annotation2)
                        toAdd.add(mergedAnnotation)
                        merged = true
                        break
                    }
                }
            }
            if (merged) break
        }

        tissueAnnotations.removeAll(toRemove)
        tissueAnnotations.addAll(toAdd)
        toRemove.each { removeObject(it, true) }
        toAdd.each { addObject(it) }
    } while (merged)

    print "Number of tissue annotations after merging: ${tissueAnnotations.size()}"
}

// Helper function to calculate the minimum distance between two annotations
double calculateDistanceEdge(def annotation1, def annotation2, double PixelSize) {
    def roi1 = annotation1.getROI()
    def roi2 = annotation2.getROI()

    // Convert ROIs to JTS Geometries
    def geometry1 = GeometryTools.roiToGeometry(roi1)
    def geometry2 = GeometryTools.roiToGeometry(roi2)

    // Calculate the minimum distance between the two geometries
    return geometry1.distance(geometry2)
}


// Merge annotations within a threshold distance (in micrometers)
def mergeAnnotations2(double micrometerThreshold = 200.0) {
    def tissueAnnotations = getAnnotationObjects().findAll { 
        it.getPathClass() != null && it.getPathClass().getName() == "Tissue" 
    }
    
    // Get the pixel size in micrometers
    def pixelSize = getCurrentImageData().getServer().getPixelCalibration().getAveragedPixelSizeMicrons()
    if (pixelSize <= 0) {
        throw new IllegalStateException("Pixel size must be greater than zero")
    }

    // Convert micrometer threshold to pixel distance
    double pixelThreshold = micrometerThreshold / pixelSize

    boolean merged
    do {
        merged = false
        def toRemove = []
        def toAdd = []

        for (int i = 0; i < tissueAnnotations.size(); i++) {
            def annotation1 = tissueAnnotations[i]

            for (int j = i + 1; j < tissueAnnotations.size(); j++) {
                def annotation2 = tissueAnnotations[j]

                // Calculate distance in pixels
                double distance = calculateDistanceEdge(annotation1, annotation2, pixelSize)

                // Compare using the pixel threshold
                if (distance < pixelThreshold) {
                    def mergedAnnotation = mergeTwoAnnotations(annotation1, annotation2)

                    if (mergedAnnotation != null) {
                        toRemove.add(annotation1)
                        toRemove.add(annotation2)
                        toAdd.add(mergedAnnotation)
                        merged = true
                        break
                    }
                }
            }
            if (merged) break
        }

        tissueAnnotations.removeAll(toRemove)
        tissueAnnotations.addAll(toAdd)
        toRemove.each { removeObject(it, true) }
        toAdd.each { addObject(it) }
    } while (merged)

    print "Number of tissue annotations after merging 2: ${tissueAnnotations.size()}"
}


// remove the large debris common in sox 10s
def removeLarge(double areaThresholdMicrometers = 10000000.0) {
    // Get the pixel size in micrometers
    def pixelSize = getCurrentImageData().getServer().getPixelCalibration().getAveragedPixelSizeMicrons()
    if (pixelSize <= 0) {
        throw new IllegalStateException("Pixel size must be greater than zero")
    }

    // Convert the area threshold to pixels
    double areaThresholdPixels = areaThresholdMicrometers / (pixelSize * pixelSize)

    // Get updated annotations
    def annotationsTissue = getAnnotationObjects()

    // Find annotations with an area greater than the pixel threshold
    def largeAnnotations = annotationsTissue.findAll { it.getROI()?.getArea() > areaThresholdPixels }

    // Remove the large annotations
    largeAnnotations.each { annotation ->
        removeObject(annotation, true)
    }
}


 
 
// WORKFLOW
// Get the current open project
def project = getProject()
if (project == null) {
    println "No project is currently open."
    return
}


// Store image name in project
def imageName = getCurrentImageData().getServer().getMetadata().getName()

// Don't use image masks
if (imageName.toLowerCase().contains(" - mask")) {
    return
}

// go
applyClassifier(project, imageName)
splitAnnotations()
removeLarge()
mergeAnnotations()

mergeAnnotations2()
