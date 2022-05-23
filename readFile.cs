FileInfo theSourceFile = null;
StringReader reader = null;
 
TextAsset posdata = (TextAsset)Resources.Load("position", typeof(TextAsset));
// puzdata.text is a string containing the whole file. To read it line-by-line:
reader = new StringReader(posdata.text);
if ( reader == null )
{
   Debug.Log("position.txt not found or not readable");
}
else
{
   // Read each line from the file
   string txt = reader.ReadLine();
   while ( txt != null )
      Debug.Log("-->" + txt);
      txt = reader.ReadLine();
}