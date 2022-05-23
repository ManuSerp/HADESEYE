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
        string[] coord = txt.Split(' ');
        x=coord[0];
        y=coord[1];
        z=coord[2];
        radius=coord[3];
        Vector3 pos = transform.position;
        pos.x = x;
        pos.y = y;
        pos.z = z;
        transform.position = pos;
        SphereCollider myCollider = transform.GetComponent<SphereCollider>();
        myCollider.radius = radius;
        txt = reader.ReadLine();
}