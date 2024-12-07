import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.deco.MaterialDeco import MaterialDeco
from sele.spider.crawler.CrawlerHandler import CrawlerHandler

class MaterialParaText(CrawlerHandler):
  '''
  Extend the required fields by existed fields
  '''
  kind = 'handler'

  @MaterialDeco()
  def resolve(self,request):
    if not request or not request.get('material'):
      return
    
    self.__replace(request)

  def __replace(self,request):
    material = request.get('material')
    paras = material.get('material_body')
    char_count = 0
    for para in paras:
      # download and deal image
      if para['type'] == 'text': 
        # replace the author
        char_count += len(para['type'])
        para['value'] = self.__get_clean_text(para['value'])

  def __get_clean_text(self,text):
    # replace the author
    #original_authors = self.schema.author_atom.get_value()
    original_authors = ['凤凰网','凤凰','环球网','环球']
    system_author = '深蓝'
    if not original_authors:
      return text

    clean_text = text
    for author in original_authors:
      clean_text = clean_text.replace(author,system_author)

    return clean_text
