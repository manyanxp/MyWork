using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace WCFHost
{
    /// <summary>
    /// MainWindow.xaml の相互作用ロジック
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            this.Closing += MainWindow_Closing;
        }

        void MainWindow_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            App.Manager.Close();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            App.Manager.Start();
        }

        private void Button_Click_1(object sender, RoutedEventArgs e)
        {

        }

        private void Button_Click_2(object sender, RoutedEventArgs e)
        {
            //_host.Say("message1");
        }

        private void Button_Click_3(object sender, RoutedEventArgs e)
        {
            App.Manager.Health();
        }

        private void Button_Click_4(object sender, RoutedEventArgs e)
        {
            App.Manager.Terminate();
        }
    }
}
