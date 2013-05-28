# biblib user form

## Document type determination

### Principals

To simplify the document type selection, we will ask many simple question to the user.

Theses questions will be represented like a tree map.

A document type can appear more than one time inside the tree...

### User first level choice

Available options:

	* Text
	* Image
	* Audio
	* Video

### "Text" sub level

Text sub levels are:

	* Article
		* JournalArticle
		* MagazineArticle
		* NewspaperArticle
		* BookReview
		* InterviewArticle
		* Annotation
		* PeriodicalIssue
	* Book
		* Book
		* ConferenceProceedings
		* Dictionary
		* Encyclopedia
		* MultiVolumeBook
	* DocumentPart
		* BookPart
		* DictionaryEntry
		* EncyclopediaArticle
	* Thesis
		* MasterThesis
		* DoctoralThesis
		* ProfessoralThesis
    * TechnicalText
    	* Patent
    	* MusicalScore
	    * Legislation
	    	* AdministrativeDocument
	    	* Hearing
	    	* Treaty
	    	* Standard
	    	* GovernmentPublication
	    	* Statute
	    	* Bill
	    	* Code
	    * LegalCase
	    	* CourtReport
	    	* Brief
	    	* LegalDecision
	    	* Hearing
    * WebEntity
    	* WebCluster
    	* WebSite
    	* WebSection
    	* WebPage
    	* WebPost
    * Event
    	* Workshop
    	* Performance
    	* Conference
    		* Speech
    		* ConferencePoster
    		* ConferenceContribution
    		* ConferencePaper
    		* ConferenceProceedings
    	* Hearing
   	* UnpublishedDocument
   		* Manual
   		* Booklet
   		* Note
   		* Report
   		* TechReport
   		* Manuscript
   		* CurriculumVitae
   		* WorkingPaper
   		* preprint
    * Other
    	* Dataset
    	* Software
    	* PhysicalObject
  		* PersonalCommunicationDocument
   			* Letter
   			* InstantMessage
   			* Email

#### Article third level

Article type determination is based on the **genre** and the **is_part_of.type** (periodical type) properties.

	if genre == "Article" :
		if is_part_of.type == "Journal" :
			return "JournalArticle"
		elsif is_part_of.type == "Newspaper" :
			return "NewspaperArticle"
		elsif is_part_of.type == "Magazine" :
			return "MagazineArticle"
		
	elif genre == "Interview" :
		return "InterviewArticle"
		
	elif genre == "Annotation" :
		return "Annotation"
		
	elif genre == "Review" :
		return "BookReview"

#### Book third level

No sub choice for Book

#### DocumentPart third level

DocumentPart type determination is based on the **is_part_of.type** properties.

	if is_part_of.type == "Book" :
		return "BookPart"
	elsif is_part_of.type == "Dictionary" :
		return "DictionaryEntry"
	elsif is_part_of.type == "Encyclopedia" :
		return "EncyclopediaEntry"

#### Thesis third level

Thesis type determination is based on the **degree** property.

	if degree == "Master" :
		return "MasterThesis"
		
	elif degree == "Doctoral" :
		return "DoctoralThesis"
		
	elif genre == "Professoral" :
		return "ProfessoralThesis"


### "Image" sub level

Image types are :

	* Artwork
	* Map
	* Chart
	* Drawing
	* Engrave
	* Painting
	* Photograph
	* Poster

### "Audio" sub level

Audio types are :

	* AudioRecording
	* AudioBook
	* AudioBroadcast
	* MusicRecording
	
### "Video" sub level

Video types are :

	* VideoRecording
	* VideoBroadcast
	* Film

