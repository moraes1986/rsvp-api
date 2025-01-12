function printData()
{
   var divToPrint=document.getElementById("example1");
   newWin= window.open("");
   newWin.document.write(divToPrint.outerHTML);
   newWin.print();
   newWin.close();
}