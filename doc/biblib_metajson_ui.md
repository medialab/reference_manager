# BibLib User Form

## 1. Document type determination

### 1.1. Principals

To simplify the document type selection, we will ask many simple question to the user.

Theses questions will be represented like a tree map.

A document type can appear more than one time inside the tree...

The UI can obtain this document type tree using the JSON-RPC method :

    {"jsonrpc":"2.0","method":"types","id":1,"params":["document_type","fr"]}

### 1.2. User first level choice

Available options:

	* Text
	* Image
	* Audio
	* Video

### 1.3. "Text" sub level

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

#### 1.3.1. Article third level

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

#### 1.3.2. Book third level

No sub choice for Book

#### 1.3.3. DocumentPart third level

DocumentPart type determination is based on the **is_part_of.type** properties.

	if is_part_of.type == "Book" :
		return "BookPart"
	elsif is_part_of.type == "Dictionary" :
		return "DictionaryEntry"
	elsif is_part_of.type == "Encyclopedia" :
		return "EncyclopediaEntry"

#### 1.3.4. Thesis third level

Thesis type determination is based on the **degree** property.

	if degree == "Master" :
		return "MasterThesis"
		
	elif degree == "Doctoral" :
		return "DoctoralThesis"
		
	elif genre == "Professoral" :
		return "ProfessoralThesis"


### 1.4. "Image" sub level

Image types are :

	* Artwork
	* Map
	* Chart
	* Drawing
	* Engrave
	* Painting
	* Photograph
	* Poster

### 1.5. "Audio" sub level

Audio types are :

	* AudioRecording
	* AudioBook
	* AudioBroadcast
	* MusicRecording
	
### 1.6. "Video" sub level

Video types are :

	* VideoRecording
	* VideoBroadcast
	* Film

## 2. Forms and Fields

When the user have chosen a document_type, the UI can obtain the Fields for this document_type using the JSON-RPC method : **types**

    {"jsonrpc":"2.0","method":"uifields","id":1,"params":["Book","fr"]}


### 2.1. UI Field

Description of each field :
 
* **property** : JSON property / key
* **labels** : dictionnay of labels using the language code as the key
* **descriptions** : Optional user contextual help for this field
* **required** : if true, than this field must be populated by the user
* **multiple** : if true than the property is a list containing the type_data
* **type_data** : basic or custom data type like :
	* text : string
	* number : integer, long, double, float…
	* date : ISO8601 date like YYYY-MM-DD, YYYY-MM, YYYY…
	* boolean : true or false
	* type : string egal to the 
* **type_source** : if the type_data is "type" than the property type_source must be set with the code / id of this type list of values. For example : identifier_type.
* **type_ui** : basic or Custom UI field type like :
	* `CharField` : input text
	* `TextField` : textarea
	* `DateField` : input text with ISO 8601 date management facilities
	* `BooleanField` : input checkbox
	* `RadioField` : input radio (using type_source for values list)
	* `DropdownField` : select (using type_source for values list)
	* `DropdownMultiField` : select with more than 1 selected value (using type_source for values list)

	* `URLField` : imput text with URL managment facilities
	* `FileField` : input file
	* `CreatorField` : custom component for Creator (author)
	* `LanguageValueField` : custom component for LanguageValue object like {"language": "fr", "value": "Bonjour"}.
	* …
* **template** : JSON template with a $ in place of the value.


### 2.2. Types list

	

## Examples and Fields by document type

### Book

#### JSON

    {
      "_id": {
        "$oid": "51adf426e218103505412805"
      }, 
      "creators": [
        {
          "agent": {
            "name_family": "Stengers", 
            "name_given": "Isabelle", 
            "rec_class": "Person", 
            "rec_metajson": 1
          }, 
          "role": "aut"
        }
      ], 
      "date_issued": "1996", 
      "publication_places": [
        "Paris"
      ], 
      "publishers": [
        "La découverte", 
        "Les Empêcheurs de penser en rond"
      ], 
      "rec_class": "Document", 
      "rec_id": "141", 
      "rec_metajson": 1, 
      "rec_source": "EndNote XML File", 
      "rec_type": "Book", 
      "title": "Cosmopolitiques - Tome 1: la guerre des sciences"
    }

#### UIFields

	

### JournalArticle

    {
      "_id": {
        "$oid": "51adf426e2181035054127f4"
      }, 
      "creators": [
        {
          "agent": {
            "name_family": "MacKenzie", 
            "name_given": "Donald", 
            "rec_class": "Person", 
            "rec_metajson": 1
          }, 
          "role": "aut"
        }, 
        {
          "agent": {
            "name_family": "Millo", 
            "name_given": "Y.", 
            "rec_class": "Person", 
            "rec_metajson": 1
          }, 
          "role": "aut"
        }
      ], 
      "date_issued": "2003", 
      "is_part_ofs": [
        {
          "rec_class": "Document", 
          "rec_metajson": 1, 
          "rec_type": "Journal", 
          "title": "American Journal of Sociology"
        }
      ], 
      "part_issue": "1", 
      "part_page_end": "145", 
      "part_page_start": "107", 
      "part_volume": "109", 
      "rec_class": "Document", 
      "rec_id": "92", 
      "rec_metajson": 1, 
      "rec_source": "EndNote XML File", 
      "rec_type": "JournalArticle", 
      "title": "Constructing a Market, Performing Theory: the Historical Sociologi of a Financial Derivatives Exchange"
    }


#### MagazineArticle

Number of references : 0

    {
        "_id": {
            "$oid": "5134b43f3b71f3102de42e21"
        }, 
        "creators": [
            {
                "name_family": "Family1", 
                "name_given": "Given2", 
                "role": "aut", 
                "type": "person"
            }, 
            {
                "name_family": "Family2", 
                "name_given": "Given2", 
                "role": "aut", 
                "type": "person"
            }
        ], 
        "date_issued": "2010", 
        "is_part_ofs": [
            {
                "rec_type": "Magazine", 
                "title": "Magazine title"
            }
        ], 
        "part_month": "12", 
        "part_page_end": "104", 
        "part_page_start": "101", 
        "rec_id": "92", 
        "rec_source": "endnote-fusion.xml", 
        "rec_type": "MagazineArticle", 
        "title": "Article title"
    }

