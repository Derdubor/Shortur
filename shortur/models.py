import datetime, random, string

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class ShortURL(Base):
    __tablename__ = 'shorturl'
    id = Column(Integer, primary_key=True)
    key = Column(String(12), unique=True, nullable=False)
    url = Column(Text, nullable=False, index=True)
    hits = relationship("ShortURLHits")
    hits_total = Column(Integer, nullable=False, default=0)

    def __init__(self, key, url, hits_total=0):
        self.key = key
        self.url = url
        self.hits_total = hits_total
        
    def got_hit(self):
        hits = DBSession.query(ShortURLHits).filter(
                ShortURLHits.shorturl_id == self.id
            ).filter( 
                ShortURLHits.date == datetime.date.today()
        ).first()
        
        if not hits:
            hits = ShortURLHits(shorturl_id=self.id, date=datetime.date.today())
            DBSession.add(hits)
        
        hits.hits += 1
        self.hits_total += 1
             
        return self.hits_total

    @classmethod
    def generate_available_key(cls, length=5):
        chars = string.ascii_letters + string.digits
        tries = 0
        
        while True:
            key = ''
            for i in range(0, length):
                key += random.choice(chars)
            
            exists = DBSession.query(cls).filter(cls.key == key).first()
            
            if not exists:
                return key
            
            tries += 1
            
            # increase length with 1 if we're unable to find any suitable ID in five tries
            if tries%5 == 0:
                length += 1

class ShortURLHits(Base):
    __tablename__ = 'shorturl_hits'
    
    shorturl_id = Column(Integer, ForeignKey('shorturl.id'), nullable=False, primary_key=True)
    date = Column(Date, nullable=False, primary_key=True)
    hits = Column(Integer, nullable=False)
    
    def __init__(self, shorturl_id, date):
        self.shorturl_id = shorturl_id
        self.date = date
        self.hits = 0
