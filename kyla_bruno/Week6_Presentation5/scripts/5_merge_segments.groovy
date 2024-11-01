// Parameters
double distanceThreshold = 1500.0  // Distance threshold in micrometers

// Retrieve all annotations of the "Tissue" class
def tissueAnnotations = getAnnotationObjects().findAll { it.getPathClass() != null && it.getPathClass().getName() == "Tissue" }

// Function to calculate Euclidean distance between annotation centroids
// Function to calculate Euclidean distance between annotation centroids
double calculateDistance(def annotation1, def annotation2) {
    double x1 = annotation1.getROI().getCentroidX()
    double y1 = annotation1.getROI().getCentroidY()
    double x2 = annotation2.getROI().getCentroidX()
    double y2 = annotation2.getROI().getCentroidY()
    return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2))
}


// Function to merge two annotations
def mergeAnnotations(def annotation1, def annotation2) {
    def roi1 = annotation1.getROI()
    def roi2 = annotation2.getROI()
    def mergedROI = ROIs.union([roi1, roi2])
    def mergedAnnotation = PathObjects.createAnnotationObject(mergedROI, annotation1.getPathClass())
    return mergedAnnotation
}

// Perform multiple rounds of merging
boolean merged
do {
    merged = false
    def remainingAnnotations = new ArrayList(tissueAnnotations)  // Copy list to avoid modification during iteration

    for (int i = 0; i < remainingAnnotations.size(); i++) {
        def annotation1 = remainingAnnotations[i]

        for (int j = i + 1; j < remainingAnnotations.size(); j++) {
            def annotation2 = remainingAnnotations[j]

            if (calculateDistance(annotation1, annotation2) < distanceThreshold) {
                // Merge the two annotations
                def mergedAnnotation = mergeAnnotations(annotation1, annotation2)

                // Remove original annotations and add merged one
                removeObject(annotation1, true)
                removeObject(annotation2, true)
                addObject(mergedAnnotation)

                // Update list with merged annotation
                tissueAnnotations.remove(annotation1)
                tissueAnnotations.remove(annotation2)
                tissueAnnotations.add(mergedAnnotation)

                merged = true  // Set flag to indicate a merge occurred
                break
            }
        }
        if (merged) break
    }
} while (merged)

print "Merging complete!"
