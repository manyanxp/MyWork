using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using WcfService;

namespace WCFClient.Services
{
    public class ProtocolInterpreter : IClientContractCallback
    {
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

        /// <summary>
        /// データ送信
        /// </summary>
        public void SendData(string message)
        {
            Console.WriteLine(message);
        }

        public void Health()
        {

        }

        public void Terminate()
        {

        }
    }
}
