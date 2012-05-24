import imp_unittest, unittest
import wtc
import wx
import os

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#print os.getpid(); raw_input('Press enter...')

#---------------------------------------------------------------------------

class DataObjTests(wtc.WidgetTestCase):
    
    def test_DataFormat(self):
        fmt1 = wx.DataFormat('my custom format')
        fmt2 = wx.DataFormat(wx.DF_TEXT)
        self.assertTrue(fmt1 != fmt2)
        fmt3 = wx.DataFormat(wx.DF_TEXT)
        self.assertTrue(fmt2 == fmt3)
        
        
        
    def test_DataFormatIDsExist(self):
        wx.DF_INVALID
        wx.DF_TEXT
        wx.DF_BITMAP
        wx.DF_METAFILE
        wx.DF_SYLK
        wx.DF_DIF
        wx.DF_TIFF
        wx.DF_OEMTEXT
        wx.DF_DIB
        wx.DF_PALETTE
        wx.DF_PENDATA
        wx.DF_RIFF
        wx.DF_WAVE
        wx.DF_UNICODETEXT
        wx.DF_ENHMETAFILE
        wx.DF_FILENAME
        wx.DF_LOCALE
        wx.DF_PRIVATE
        wx.DF_HTML
        wx.DF_MAX


        
    def test_DataObjectGetAllFormats(self):
        class MyDataObject(wx.DataObject):
            def __init__(self):
                wx.DataObject.__init__(self)
                self.myFormats = [wx.DataFormat(wx.DF_TEXT), 
                                  wx.DataFormat(wx.DF_UNICODETEXT)]
                
            def GetAllFormats(self, d):
                return self.myFormats
            
            def GetFormatCount(self, d):
                return len(self.myFormats)
                
        data = MyDataObject()
        if hasattr(data, '_testGetAllFormats'):
            data._testGetAllFormats()
        
        
        
    def test_DataObject(self):
        class MyDataObject(wx.DataObject):
            def __init__(self, value=''):
                wx.DataObject.__init__(self)
                self.myFormats = [wx.DataFormat(wx.DF_TEXT)]                
                self.myData = wtc.mybytes(value)
                
            def GetAllFormats(self, d):
                return self.myFormats            
            def GetFormatCount(self, d):
                return len(self.myFormats)  
            def GetPreferredFormat(self, d):
                return self.myFormats[0]
            def GetDataSize(self, format):
                return len(self.myData)
            
            def GetDataHere(self, format, buf):
                # copy our local data value to buf
                assert isinstance(buf, memoryview)
                buf[:] = self.myData
                return True
                            
            def SetData(self, format, buf):
                # copy from buf to our local data value
                assert isinstance(buf, memoryview)
                self.myData = buf.tobytes()
                return True
            
        # copy
        data1 = MyDataObject('This is some data.')
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data1)
            wx.TheClipboard.Close()
               
        # paste 
        data2 = MyDataObject()
        if wx.TheClipboard.Open():
            wx.TheClipboard.GetData(data2)
            wx.TheClipboard.Close()
        
        self.assertEqual(data1.myData, data2.myData)
        
        
        
    def test_DataObjectSimple1(self):
        df = wx.DataFormat(wx.DF_TEXT)
        dobj = wx.DataObjectSimple(df)
        self.assertTrue(dobj.GetFormatCount() == 1)
        self.assertTrue(dobj.GetFormat() == df)
        self.assertTrue(dobj.GetAllFormats()[0] == df)

        
    def test_DataObjectSimple2(self):
        class MyDataObject(wx.DataObjectSimple):
            def __init__(self, value=''):
                wx.DataObjectSimple.__init__(self)
                self.SetFormat(wx.DataFormat(wx.DF_TEXT))
                self.myData = wtc.mybytes(value)
                
            def GetDataSize(self):
                return len(self.myData)
            
            def GetDataHere(self, buf):
                # copy our local data value to buf
                assert isinstance(buf, memoryview)
                buf[:] = self.myData
                return True
                            
            def SetData(self, buf):
                # copy from buf to our local data value
                assert isinstance(buf, memoryview)
                self.myData = buf.tobytes()
                return True
            
        # copy
        data1 = MyDataObject('This is some data.')
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data1)
            wx.TheClipboard.Close()
              
        # paste  
        data2 = MyDataObject()
        if wx.TheClipboard.Open():
            wx.TheClipboard.GetData(data2)
            wx.TheClipboard.Close()
        
        self.assertEqual(data1.myData, data2.myData)
            
        
            
    def test_CustomDataObject(self):
        import pickle
        data1 = list(range(10))
        obj = wx.CustomDataObject('my custom format')
        obj.SetData(pickle.dumps(data1))
        data2 = pickle.loads(obj.GetData().tobytes())
        self.assertEqual(data1, data2)
    
    
    
    def test_DataObjectComposite(self):
        do = wx.DataObjectComposite()
        df1 = wx.DataFormat("data type 1")
        df2 = wx.DataFormat("data type 2")
        d1 = wx.CustomDataObject(df1)
        d2 = wx.CustomDataObject(df2)
        do.Add(d1, True)
        do.Add(d2)
        
        self.assertTrue(do.GetPreferredFormat() == df1)
        d3 = do.GetObject(df2)
        self.assertTrue(isinstance(d3, wx.CustomDataObject))
        self.assertTrue(d3 is d2)
        

    def test_BitmapDataObject(self):
        do = wx.BitmapDataObject()
        do.Bitmap = wx.Bitmap(pngFile)
        self.assertTrue(do.GetBitmap().IsOk())
        self.assertTrue(do.Bitmap.IsOk())
        
        
    def test_TextDataObject(self):
        data = "This is some data"
        do = wx.TextDataObject(data)
        self.assertEqual(do.GetText(), data)
        self.assertEqual(do.Text, data)
        self.assertAlmostEqual(do.GetTextLength(), len(data), delta=1)
        self.assertAlmostEqual(do.TextLength, len(data), delta=1)
        
        
    def test_URLDataObject(self):
        url = 'http://wxPython.org/'
        do = wx.URLDataObject()
        do.URL = url
        self.assertEqual(do.GetURL(), url)
        self.assertEqual(do.URL, url)
        
        
    def test_FileDataObject(self):
        do = wx.FileDataObject()
        do.AddFile('filename1')
        do.AddFile('filename2')
        do.AddFile('filename3')

        names = do.GetFilenames()
        self.assertTrue(len(names) == 3)
        self.assertTrue(names[0] == 'filename1')
        self.assertTrue(names == do.Filenames)
        
        
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
