library(tm)
library(lsa)

setNA<- function(x,docNames){
  doc_labels = docNames
  k=1
  while(k<=nrow(x)){
    doc_labels[k] = unlist(strsplit(docNames[k]," "))[1]
    k=k+1
  }
  
  #print(doc_labels)
  i=1
  j=1
  while(i<=nrow(x)-1){
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

find_distance<-function(myArr){
  
    print(length(myArr))
    sim_matrix = array(0,c(length(myArr),length(myArr)))
    print(sim_matrix)
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

inputData <- read.csv("/home/gandy1l/data mining/labels_syn_labels_values.csv",stringsAsFactors=FALSE,head=TRUE)
#m<-list(Content="labelText",Topic="docName")

docnames = labelData$docName
valuesArr = as.numeric(inputData$numValues)

#use function here...
sim_matrix <- find_distance(valuesArr)
#print(sim_matrix)
#sim_matrix <- setNA(sim_matrix,docnames)
#print(summary(sim_matrix))
dimnames(sim_matrix) = list(docnames, docnames)
write.csv(abs(1-sim_matrix),"/home/gandy1l/data mining/values_sim.csv")
#find dissimilarity matrix

#print sim_matrix out to csv
