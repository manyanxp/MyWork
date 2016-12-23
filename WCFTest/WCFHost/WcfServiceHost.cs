using System;
using System.ServiceModel;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using Cosmweb.Net.WCF;

namespace WCFHost
{
    [ServiceBehavior(InstanceContextMode = InstanceContextMode.PerSession,
        ConcurrencyMode = ConcurrencyMode.Multiple, UseSynchronizationContext = false)]
    public class WcfServiceHost : WcfHostBase<IServerContract>, IServerContract
    {
        #region Singleton
        private static WcfServiceHost single = new WcfServiceHost();
        private WcfServiceHost()
        {
            base.Create(typeof(WcfServiceHost),
                        "net.tcp://localhost:8080/ServerService",
                        base.MaxMessageSize);
        }
        public static WcfServiceHost Instance { get { return WcfServiceHost.single; } }
        #endregion

        /// <summary>
        /// オープンイベント
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public override void _host_Opened(Object sender, EventArgs e)
        {
            Console.WriteLine("Wcf Server オープン");
        }

        /// <summary>
        /// クローズイベント
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public override void _host_Closed(object sender, EventArgs e)
        {
            base._host_Closed(sender, e);
            Console.WriteLine("Wcf Server クローズ");
        }

        /// <summary>
        /// 異常イベント
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public override void _host_Faulted(Object sender, EventArgs e)
        {
            base._host_Faulted(sender, e);
            Console.WriteLine("Wcf Server 異常?");
        }

        public string Message { get; set; }

        /// <summary>
        /// メッセージ設定
        /// </summary>
        /// <param name="message"></param>
        public void SetMessage(string message)
        {
            Message = message;
        }

        /// <summary>
        /// メッセージ取得
        /// </summary>
        /// <param name="message"></param>
        public string GetMessage()
        {
            return Message;
        }


        private string clientName = "";
        private int callCount = 0;


        public void Login(string clientName)
        {
            if (this.clientName.Equals(clientName) == false)
            {
                this.clientName = clientName;
            }
            else
            {
                Console.WriteLine("接続済み");
            }

            Instance.Host.Credentials
        }

        public string GetData()
        {
            callCount++;
            var mes = string.Format("クライアント名:{0} 呼び出し回数:{1}", this.clientName, this.callCount);
            Console.WriteLine(mes);
            return mes;
        }

        public void Logout()
        {
            this.clientName = "";
            this.callCount = 0;
        }
    }
 }
