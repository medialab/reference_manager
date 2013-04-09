# MetaJson manuel

## User form type determination

### MAIN level

    TEXT
    IMAGE
    AUDIO
    VIDEO
    
### TEXT second level

    Article
    Book
    DocumentPart
    Thesis
    TechnicalText
    WebText
    Event
    PhysicalObject
    ElectronicDocument
    UnpublishedDocument
    PersonalCommunicationDocument
    

#### TEXT / Article third level

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
		
#### TEXT / Book third level

No sub choice for Book

#### TEXT / DocumentPart third level

DocumentPart type determination is based on the **is_part_of.type** properties.

	if is_part_of.type == "Book" :
		return "BookPart"
	elsif is_part_of.type == "Dictionary" :
		return "DictionaryEntry"
	elsif is_part_of.type == "Encyclopedia" :
		return "EncyclopediaEntry"

#### TEXT / Thesis third level

Thesis type determination is based on the **degree** property.

	if degree == "Master" :
		return "MasterThesis"
		
	elif degree == "Doctoral" :
		return "DoctoralThesis"
		
	elif genre == "Professoral" :
		return "ProfessoralThesis"
		
#### TEXT / TechnicalText third level

	Patent
	MusicalScore
	Legislative
	LegalCase
	

#### TEXT / WebText third level



#### TEXT / Event third level



#### TEXT / PhysicalObject third level



#### TEXT / ElectronicDocument third level



#### TEXT / UnpublishedDocument third level



#### TEXT / PersonalCommunicationDocument third level



### IMAGE second level

Image types are :

	Artwork
	Chart
	Drawing
	Engrave
	Map
	Painting
	Photograph
	Poster
	

### AUDIO second level

AUDIO types are :

	AudioRecording
	AudioBook
	AudioBroadcast
	MusicRecording
	
### VIDEO second level

VIDEO types are :

	VideoRecording
	VideoBroadcast
	Film
	

## Fields and examples by type

### Article

#### JournalArticle

Number of references : 69


    {
        "_id": {
            "$oid": "5134b43f3b71f3102de42e20"
        }, 
        "contributors": [
            {
                "name_family": "Family1", 
                "name_given": "Given1", 
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
        "date_issued": "2003", 
        "is_part_of": [
            {
                "rec_type": "Journal", 
                "title": "Journal title"
            }
        ], 
        "part_issue": "1", 
        "part_page_end": "145", 
        "part_page_start": "107", 
        "part_volume": "109", 
        "rec_id": "92", 
        "rec_source": "endnote-fusion.xml", 
        "rec_type": "JournalArticle", 
        "title": "Article title"
    }


#### MagazineArticle

Number of references : 0

    {
        "_id": {
            "$oid": "5134b43f3b71f3102de42e21"
        }, 
        "contributors": [
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
        "is_part_of": [
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

#### NewspaperArticle

Number of references : 0

    {
        "_id": {
            "$oid": "5134b43f3b71f3102de42e21"
        }, 
        "contributors": [
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
        "date_issued": "2010-12-31", 
        "is_part_of": [
            {
                "rec_type": "Newspaper", 
                "title": "Newspaper title"
            }
        ], 
        "part_page_end": "101", 
        "part_page_start": "101", 
        "part_column": "2"
        "rec_id": "92", 
        "rec_source": "endnote-fusion.xml", 
        "rec_type": "NewspaperArticle", 
        "title": "Article title"
    }
    
#### InterviewArticle

Number of references : 0

    {
        "_id": {
            "$oid": "5134b43f3b71f3102de42e21"
        }, 
        "contributors": [
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
        "date_issued": "2010-12-31", 
        "is_part_of": [
            {
                "rec_type": "Newspaper", 
                "title": "Newspaper title"
            }
        ], 
        "part_page_end": "101", 
        "part_page_start": "101", 
        "part_column": "2"
        "rec_id": "92", 
        "rec_source": "endnote-fusion.xml", 
        "rec_type": "NewspaperArticle", 
        "title": "Article title"
    }
