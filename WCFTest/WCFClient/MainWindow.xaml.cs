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
using System.ServiceModel;

namespace WCFClient
{
    /// <summary>
    /// MainWindow.xaml の相互作用ロジック
    /// </summary>
    public partial class MainWindow : Window
    {
        ClientService _client = null;

        public MainWindow()
        {
            InitializeComponent();

            try
            {
                _client = ClientService.Instance;
                _client.Test += _client_Test;
                //_client = new WcfServiceClient();
            }
            catch( Exception ex)
            {
                MessageBox.Show(ex.StackTrace);
            }
        }

        void _client_Test(object sender, EventArgs e)
        {
            this.Dispatcher.BeginInvoke(new Action(() => {
                MessageBox.Show("切断！");
            }));
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            var channel = (_client.Host as IDuplexContextChannel);
            if (  channel != null )
            {
                Logger.DebugLog.LogInfo(channel.State.ToString());
            }
            _client.Open();   
        }

        private void Button_Click_1(object sender, RoutedEventArgs e)
        {
            _client.Close();
        }

        private void Button_Click_2(object sender, RoutedEventArgs e)
        {

            _client.Join();
            

        }

        private void Button_Click_3(object sender, RoutedEventArgs e)
        {
            _client.Host.Terminate();
        }
    }
}
