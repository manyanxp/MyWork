using System;
using System.ServiceModel;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using Cosmweb.Net.WCF;

namespace WCFClient
{
    public class WcfServiceClient : WcfClientBase<IServerContract>
    {
        #region Singleton
        private static WcfServiceClient single = new WcfServiceClient();
        private WcfServiceClient()
        {
            var serverUrl = "net.tcp://localhost:8080/ServerService";
            base.CreateChannel(serverUrl);
        }
        public static WcfServiceClient Instance { get { return WcfServiceClient.single; } }
        #endregion

        public string Message { get; set; }

        /// <summary>
        /// クローズイベント（ログ出力のみ）
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public override void OnClosed(object sender, EventArgs e)
        {
            base.OnClosed(sender, e);
            Console.WriteLine("WCF Serverとの接続がクローズしました.");
        }

        /// <summary>
        /// オープンイベント（ログ出力のみ）
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public override void OnOpened(object sender, EventArgs e)
        {
            base.OnOpened(sender, e);
            Console.WriteLine("WCF Serverと接続をオープンしました.");
            var service = (this.Server as IClientChannel);
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
        public override void OnFaulted(object sender, EventArgs e)
        {
            // 後処理必要なので基底クラスのメソッド呼出し.
            base.OnFaulted(sender, e);
            Console.WriteLine("WCF Serverと接続が異常となりました.");
        }

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
    }
}
