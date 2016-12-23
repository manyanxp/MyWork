using System;
using System.ServiceModel;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using Cosmweb.Net.WCF;
using WcfService;
using System.ServiceModel.Description;
using WCFClient.Logger;

namespace WCFClient
{
    public class ClientService : WcfClientBase<IServerContract>
    {
        public event EventHandler Test = delegate { };
        #region Singleton
        private static ClientService single = new ClientService();
        private ClientService()
        {
            var serverUrl = "net.tcp://localhost:8080/ServerService";
            this.CallBack = new InstanceContext( new Services.ProtocolInterpreter() );
            this.CreateChannel(serverUrl);
        }
        public static ClientService Instance { get { return ClientService.single; } }
        #endregion

        /// <summary>
        /// クローズイベント（ログ出力のみ）
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected override void OnClosed(object sender, EventArgs e)
        {
            base.OnClosed(sender, e);
            Logger.DebugLog.LogInfo("WCF Serverとの接続がクローズしました.");
            if( Test != null)
            {
                Test(this, new EventArgs());
            }
        }

        /// <summary>
        /// オープンイベント（ログ出力のみ）
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected override void OnOpened(object sender, EventArgs e)
        {
            base.OnOpened(sender, e);
            Logger.DebugLog.LogInfo("WCF Serverと接続をオープンしました.");
            var service = (this.Host as IClientChannel);
            if( service == null )
            {
                return;
            }

            Console.WriteLine(service.InputSession.Id);
        }

        /// <summary>
        /// 異常イベント(Serverとの接続が切れた場合）
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected override void OnFaulted(object sender, EventArgs e)
        {
            // 後処理必要なので基底クラスのメソッド呼出し.
            base.OnFaulted(sender, e);
            Logger.DebugLog.LogInfo("WCF Serverと接続が異常となりました.");
        }

        public void Join()
        {
            Instance.Host.Join(Guid.NewGuid());
        }
    }
}
