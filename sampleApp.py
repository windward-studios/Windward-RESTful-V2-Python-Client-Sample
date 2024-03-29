
from windwardrestapi.Model import ParameterValue, Template, Parameter, Xml_10DataSource, SqlDataSource
from windwardrestapi.Api import WindwardClient as client
import os
import time
import base64
import zipfile
if __name__ == '__main__':
   '''
   Create a client object by callig the WindwardClient() constructor
   Pass in the url to your RESTful engine to the constructor as shown bellow
   '''
   testClient = client.WindwardClient("http://localhost:61742/")

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
   # testSqlDS = SqlDataSource.SqlDataSource(name="SqlServer", className="System.Data.SqlClient", connectionString="Data Source=mssql.windward.net;Initial Catalog=Northwind;User ID=demo;Password=demo")

   'Set the input parameter for the template as a parameter object and pass in to template constructor'
   # testParam = Parameter.Parameter(name="varName1", wrappedValue=ParameterValue.ParameterValue(paramType="string", rawValue="zaid"))

   'Create the testTemplate object using the Template.Template() constructor'
   testTemplate = Template.Template(data=file, outputFormat=Template.outputFormatEnum.DOCX, datasources=testXmlDS)

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
   testGetDocumentMeta = testClient.getDocumentMeta(testGetDocument.guid)
   print("testGetDocumentMeta: ", testGetDocumentMeta.toDict())
   # USE THIS CODE TO WRITE THE ENCODED DATA TO FILE (file will be called output)
   # filePath = "files/output."+testTemplate.outputFormat
   # with open(, "wb") as fh:
   #    fh.write(filePath, base64.standard_b64decode(testGetDocument.data))
   #    assert(zipfile.is_zipfile(filePath))
   #    zip = zipfile.ZipFile(filePath)
   #    assert(zip.read("word/document.xml") is not None)


   #  USE THIS CODE TO WRITE FILESTREAM TO FILE. (file will have guid as file name)
   # testGetDocumentMeta = testClient.getDocumentMeta(testGetDocument.guid)
   # testFileStream = testClient.getDocumentFile(testGetDocument.guid)
   # filePath = "files/"+testGetDocument.guid+"."+ testTemplate.outputFormat
   # with open(filePath, "wb") as file:
   #    file.write(testFileStream)

   ############################
          # METRICS #
   ###########################
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
