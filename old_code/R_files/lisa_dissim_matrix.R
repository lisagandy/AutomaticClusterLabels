library(tm)
library(lsa)
library(cluster)

normalize <- function(x) { 
  x <- sweep(x, 2, apply(x, 2, min)) 
  sweep(x, 2, apply(x, 2, max), "/") 
} 

find_distance<-function(myArr){

  sim_matrix = array(0,c(length(myArr),length(myArr)))
  #print(sim_matrix)
  i=1
  while (i<=length(myArr)-1){
    j=i+1
    while(j<=length(myArr)){
      sim_matrix[i,j]=abs(myArr[i]-myArr[j])
      sim_matrix[j,i] = sim_matrix[i,j]
      j=j+1
    }
    i=i+1
  }
  diag(sim_matrix)=1
  return(as.matrix(sim_matrix))
}


setZero<- function(x,docNames){
    doc_labels = docNames
    k=1
    while(k<=nrow(x)){
        doc_labels[k] = unlist(strsplit(docNames[k],"_"))[1]
        k=k+1
    }

    #print(doc_labels)
    i=1
    j=1
    while(i<=nrow(x)-1){par
      j=i+1
      while(j<=nrow(x)){
        if (identical(doc_labels[i],doc_labels[j]) == TRUE){
             x[i,j]=NA
             x[j,i]=NA
         }
       j=j+1
      }
      i=i+1
    }
   
  #print(x)
  return(x)
}

#get label text
labelData <- read.csv("/home/gandy1l/data mining/input_csvs/labels_syn_labels_values.csv",stringsAsFactors=FALSE,head=TRUE)
m<-list(Content="labelText",Topic="docName")
myReader<-readTabular(mapping=m)
corpusLabel<-Corpus(DataframeSource(labelData),readerControl=list(reader=myReader))

#set docnames
docnames = labelData$docName

#get values text
m<-list(Content="valuesText",Topic="docName")
myReader<-readTabular(mapping=m)
corpusValues<-Corpus(DataframeSource(labelData),readerControl=list(reader=myReader))

#get num values and create dissim matrix for num values
valuesData <- labelData$numValues#read.csv("/home/gandy1l/data mining/input_csvs/labels_syn_labels_values.csv",stringsAsFactors=FALSE,head=TRUE)
valuesArr = as.numeric(valuesData)
dissim_num_values_matrix <- abs(1 - find_distance(valuesArr))
dissim_num_values_matrix[is.na(dissim_num_values_matrix)] <- 1000

#work on the two text fields (labels and values)
corpusLabel <- tm_map(corpusLabel, tolower)
corpusValues <- tm_map(corpusValues, tolower)

## Eliminating Extra White Spaces
corpusLabel <- tm_map(corpusLabel, stripWhitespace)
corpusValues <- tm_map(corpusValues, tolower)

#create a document term matrix, and then find the tf/idf scores for each term
#for both labels and values
myLengths = c(1,Inf)
dtm <- TermDocumentMatrix(corpusLabel,control=list(stopWords=FALSE,removeNumbers=FALSE,removePunctuation=FALSE,wordLengths=myLengths))
dtm_tf <- weightTf(dtm)
matLabels = as.matrix(dtm_tf)

dtm <- TermDocumentMatrix(corpusValues,control=list(stopWords=FALSE,removeNumbers=FALSE,removePunctuation=FALSE,wordLengths=myLengths))
dtm_tf <- weightTf(dtm)
matValues = as.matrix(dtm_tf)

#create dissimilarity matrix
dissim_labels_matrix <- abs(1 - cosine(matLabels))
dissim_values_matrix <- abs(1 - cosine(matValues))
dissim_values_matrix[is.na(dissim_values_matrix)] <- 1
dissim2 = (2 * normalize(dissim_labels_matrix)) + (3 * normalize(dissim_num_values_matrix)) + (5* normalize(dissim_values_matrix))

dimnames(dissim2) = list(docnames,docnames)

#determine number of clusters
dissim2 = (20*normalize(dissim_labels_matrix)) + (normalize(dissim_values_matrix)) #+ normalize(dissim_num_values_matrix)
dissim2 = dissim_labels_matrix
wss <- (nrow(dissim2)-1)*sum(apply(dissim2,2,var))
for (i in 2:50) wss[i] <- sum(kmeans(dissim2, 
                                     centers=i)$withinss)
plot(1:50, wss, type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares")


dimnames(dissim2) = list(docnames,docnames)
cluster<- agnes(dissim2,diss="TRUE",method="ward")
#cluster<-clara(dissim2,25)




#plot(cluster)
pdf(file="/home/gandy1l/data mining/plots/dendrogram.pdf", height=10, width=30)
plot(cluster,ask = FALSE, which.plots = NULL)
groups <- cutree(cluster, k=35) # cut tree into 5 clusters
# draw dendogram with red borders around the 5 clusters 
rect.hclust(cluster, k=35, border="red")
dev.off()

sapply(unique(groups),function(g)docnames[groups == g])
#write.csv(abs(1-sim_matrix),"/home/gandy1l/data mining/label_dissim.csv")
#find dissimilarity matrix

#print sim_matrix out to csv
