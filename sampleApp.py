
from windwardrestapi.Model import ParameterValue, Template, Parameter, Xml_10DataSource
from windwardrestapi.Api import WindwardClient as client
import os
# from windwardrestapi.Model.ParameterValue import ParameterValue
# from windwardrestapi.Model.Template import Template
# from windwardrestapi.Model.Parameter import Parameter
# from windwardrestapi.Model.Xml_10DataSource import Xml_10DataSource

import time

if __name__ == '__main__':
   '''
   Create a client object by callig the WindwardClient() constructor
   Pass in the url to your RESTful engine to the constructor as shown bellow
   '''
   testClient = client.WindwardClient("http://localhost:64228/")

   'To check the version of the restful engine, use the client.getVersion() method'
   testVersion = testClient.getVersion()

   'Print the Version object as a string to the console'
   print(testVersion.toString())

   ############################
         # TEMPLATE #
   ############################

   file = os.path.abspath("./files/Manufacturing.docx")
   data = os.path.abspath("./files/Manufacturing.xml")

   'Create a test xml Datasource object'
   testXmlDS = Xml_10DataSource.Xml_10DataSource(name="MANF_DATA_2009", data=data)

   'Set the input parameter for the template as a parameter object and pass in to template constructor'
   testParam = Parameter.Parameter(name="varName1", wrappedValue=ParameterValue.ParameterValue(paramType="string", rawValue="zaid"))

   'Create the testTemplate object using the Template.Template() constructor'
   testTemplate = Template.Template(data=file, outputFormat=Template.outputFormatEnum.DOCX, datasources=testXmlDS, parameters=testParam)

   ############################
         # DOCUMENT #
   ############################
   'Post the template to be processed by the engine by calling postDocument(Template)'
   testDocument = testClient.postDocument(testTemplate)
   print("GUID: ", testDocument.guid)
   'Before retrieving the processed document we have to make sure its been processed'
   while True:
      testDocumentStatus = testClient.getDocumentStatus(testDocument.guid)
      'The document is ready when the status is 302 (this is different for different endpoints'
      if testDocumentStatus != 302:
         print("Not ready: ", testDocumentStatus)
         time.sleep(1)
      else:
         print("Ready: ", testDocumentStatus)
         break
   'Now we get the document'
   testGetDocument = testClient.getDocument(testDocument.guid)
   print("testGetDocument Guid: ", testGetDocument.guid)

   ############################
          # METRICS #
   ############################
   'Get the metrics of the template posted by using the postMetrics method'
   testMetricsPost = testClient.postMetrics(testTemplate)
   print("testMetricsPost Guid: ", testMetricsPost.guid)

   'Same as before we have to wait for the post metrics request to complete'
   while True:
      testMetricsStatus = testClient.getMetricsStatus(testMetricsPost.guid)
      if testMetricsStatus != 302:
         time.sleep(1)
      else:
         break
   'Once complete we can get the metrics'
   testGetMetrics = testClient.getMetrics(testMetricsPost.guid)
   print("METRICS\n", testGetMetrics.toDict())

   'To delete the metrics use the deleteMetrics(Guid) method'
   testMetricsDelete = testClient.deleteMetrics(testGetMetrics.guid)
   print("Metrics delete status: ", testMetricsDelete)

   ############################
           # TAGTREE #
   ############################
   'Post the tagTree for processing by calling the postTagTree(Template) method'
   testPostTagTree = testClient.postTagTree(testTemplate)
   'Wait for processing to complete'
   while True:
      testTagTreeStatus = testClient.getTagTreeStatus(testPostTagTree.guid)
      if testTagTreeStatus != 200:
         print("Not ready: ", testTagTreeStatus)
         time.sleep(1)
      else:
         print("Ready: ", testTagTreeStatus)
         break
   'Once successful, get the tagTree'
   testGetTagTree = testClient.getTagTree(testPostTagTree.guid)
   print("TAGTREE\n", testGetTagTree.toDict())

   'Delet the tagTree'
   testTagTreeDelete = testClient.deleteTagTree(testPostTagTree.guid)
   print("TagTree delete status: ", testTagTreeDelete)
