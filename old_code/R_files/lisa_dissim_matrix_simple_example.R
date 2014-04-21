library(tm)

stagger_cosine<-function(x,docNames){
		
	 	co = array(NA,c(nrow(x), nrow(x)))
        dimnames(co) = list(docNames, docNames)
        i<- 1
        
        while(i<=nrow(x)-1){
        	curr_x_squared = sqrt(sum(x[i,] * x[i,]))
        	label1 = unlist(strsplit(docNames[i]," "))[1]
			j <- i+1
        	while (j<=nrow(x)){
        		label2 = unlist(strsplit(docNames[j]," "))[1]
        		if (identical(label1,label2) == FALSE){
        			curr_y_squared = sqrt(sum(x[j,] * x[j,]))
        			numerator = sum(x[i,] * x[j,])
        			denominator = ((curr_x_squared) * (curr_y_squared))
        			co[i,j] = numerator / denominator;
        			co[j,i] = co[i,j]
        			}#end of if statement		
        		j<-j+1
                }#end of inner for loop
        	i<-i+1
        }#end of outer for loop
		
        diag(co) = 1
		return(as.matrix(co))
}


labelData <- read.csv("/Users/lisa/Desktop/data mining/labels_simple.csv",stringsAsFactors=FALSE,head=TRUE)
m<-list(Content="labels",Topic="docnumber")
myReader<-readTabular(mapping=m)
(corpus<-Corpus(DataframeSource(labelData),readerControl=list(reader=myReader)))

#lower text
corpus <- tm_map(corpus, tolower)
corpus[[1]]

# Stemming
corpus <- tm_map(corpus, stemDocument)
corpus[[1]]

## Eliminating Extra White Spaces
corpus <- tm_map(corpus, stripWhitespace)
corpus[[1]]

#create a document term matrix, and then find the tf/idf scores for each term
myLengths = c(1,Inf)
dtm <- DocumentTermMatrix(corpus,control=list(stopWords=FALSE,removeNumbers=FALSE,removePunctuation=FALSE,wordLengths=myLengths))


dtm_tf <- weightTf(dtm)
mat = as.data.frame(as.matrix(dtm_tf))
docnames = labelData$docnumber

#use function here...
sim_matrix <- stagger_cosine(mat,docnames)

