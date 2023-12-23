/**
 * Starts a unique session of Google Chrome and waits until the session closes to exit.
 * I call this from a Python script and wait on it. When it closes, the user data directory
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
            var proc = new Process();
            proc.StartInfo.FileName = args[0];
            proc.StartInfo.Arguments = $"chrome://newtab --user-data-dir=\"{args[1]}\"";
            proc.Start();
            proc.WaitForExit();
            Console.WriteLine(proc.ExitCode.ToString());
            proc.Close();
        }
    }
}
