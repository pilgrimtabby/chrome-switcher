/**
 * Start a unique session of Google Chrome and waits until the Chrome session closes to exit.
 * The Python script calls this and waits for it to finish. When it closes, the user data directory
 * is deleted by the script.
 * args[0]: Path to chrome.exe.
 * args[1]: Desired user data directory path.
 */
using System;
using System.Diagnostics;

namespace OpenTempChrome
{
    internal class Program
    {
        static void Main(string[] args)
        {
            #if DEBUG
                args = new[] { "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe", 
                               "C:\\Users\\test" };
            # endif
            var chrome = new Process();
            chrome.StartInfo.FileName = args[0];
            chrome.StartInfo.Arguments = $"chrome://newtab --user-data-dir=\"{args[1]}\"";
            chrome.Start();
            chrome.WaitForExit();
            Console.WriteLine(chrome.ExitCode.ToString());
            chrome.Close();
        }
    }
}
