using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using WCFHost.Interpreter;

namespace WCFHost
{
    public class ControlManager
    {
        private MainWindow View { get; set; }
        private Interpreter.ProtocolInterpreter Interpreter { get; set; }
            

        private object objSync = new object();

        public ControlManager()
        {
            Interpreter = ProtocolInterpreter.Instance;
        }
        
        public void Close()
        {
            Interpreter.Close();
        }

        public void Start()
        {
            Interpreter.Start();
        }

        public void Terminate()
        {
            Interpreter.Terminate();
        }

        public void Health()
        {
            Interpreter.Health();
        }
    }
}
