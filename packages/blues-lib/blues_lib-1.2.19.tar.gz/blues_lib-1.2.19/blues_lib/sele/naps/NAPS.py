import sys,os,re
from abc import ABC,abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.reader.ifeng.IFengSchemaFactory import IFengSchemaFactory
from schema.reader.thepaper.ThePaperSchemaFactory import ThePaperSchemaFactory
from sele.spider.MaterialSpider import MaterialSpider    
from sele.publisher.StandardPublisher import StandardPublisher

class NAPS(ABC):
  '''
  1. Crawl a materail
  2. Login the publish page
  3. Publish
  4. Set published log
  '''
  def __init__(self):
    # the count by all channels excepted to publish
    self.publish_plan = 0
    self.total = 0

    self.set_publish_plan()
    self.set_total()

  def set_publish_plan(self):
    self.publish_plan = {
      'events':1,
    }

  def set_total(self):
    total = 0
    for channel,count in self.publish_plan.items():
      total+=count
    self.total = total
  
  def execute(self):
    self.spide()
    self.publish()
  
  def publish(self):
    loginer = self._get_loginer()
    models = self._get_models()
    publisher= StandardPublisher(models,loginer)
    publisher.publish()

  def prepublish(self):
    loginer = self._get_loginer()
    models = self._get_models()
    publisher= StandardPublisher(models,loginer)
    publisher.prepublish()

  @abstractmethod
  def _get_loginer(self):
    pass

  @abstractmethod
  def _get_models(self):
    pass

  def spide(self):
    '''
    Crawl a material
    Return:
      {bool}
    '''
    factory = ThePaperSchemaFactory()
    schema1 = factory.create_news('intl')

    factory = IFengSchemaFactory()
    schema2 = factory.create_tech_news()
    schema3 = factory.create_tech_outpost()
    schema4 = factory.create_hot_news()

    schemas = [schema2,schema3,schema4,schema1]

    spider = MaterialSpider(schemas,self.total)
    return spider.spide()
 


