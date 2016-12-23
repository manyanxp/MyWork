using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.Linq;
using System.Windows;
namespace WCFHost
{
    /// <summary>
    /// App.xaml の相互作用ロジック
    /// </summary>
    public partial class App : Application
    {
        static ControlManager _manager = new ControlManager();
        public static ControlManager Manager { get{return _manager;}}
    }
}
