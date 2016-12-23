using System;
using System.ServiceModel;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using Cosmweb.Net.WCF;
using WcfService;
using System.Timers;
using WCFHost.Logger;

namespace WCFHost.Services
{
    public partial class ProtocolInterpreter : WcfHostBase<IServerContract>, IServerContract
    {
        #region Singleton
        private static ProtocolInterpreter single = new ProtocolInterpreter();
        private ProtocolInterpreter()
        {
            base.Create(typeof(Services.ProtocolInterpreter),
                        "net.tcp://localhost:8080/ServerService",
                        base.DefaultMaxMessageSize);
        }
        public static ProtocolInterpreter Instance { get { return ProtocolInterpreter.single; } }
        #endregion

        /// <summary>
        /// オープンイベント
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public override void _host_Opened(Object sender, EventArgs e)
        {
            DebugLog.LogInfo("Wcf Server オープン 状態[" + Host.State.ToString() + "]");
        }

        /// <summary>
        /// クローズイベント
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public override void _host_Closed(object sender, EventArgs e)
        {
            base._host_Closed(sender, e);
            DebugLog.LogInfo("Wcf Server クローズ 状態[" + Host.State.ToString() + "]");
        }

        /// <summary>
        /// 異常イベント
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public override void _host_Faulted(Object sender, EventArgs e)
        {
            base._host_Faulted(sender, e);
            DebugLog.LogInfo("Wcf Server 異常? 状態[" + Host.State.ToString() + "]");
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public override void _host_UnknownMessageReceived(object sender, UnknownMessageReceivedEventArgs e)
        {
            Host.Abort();

            DebugLog.LogInfo("Wcf Server 不明な情報受信? 状態[" + Host.State.ToString() + "]");
        }
    }

    [ServiceBehavior(InstanceContextMode = InstanceContextMode.PerSession,
        ConcurrencyMode = ConcurrencyMode.Multiple)]
    public partial class ProtocolInterpreter
    {   
        Timer _healthTimer;

        /// <summary>
        /// 
        /// </summary>
        public void CreateHealthTimer()
        {
            _healthTimer = new Timer();
            _healthTimer.Interval = 5000;
            _healthTimer.Elapsed += _healthTimer_Elapsed;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        void _healthTimer_Elapsed(object sender, ElapsedEventArgs e)
        {
            Console.WriteLine("ヘルス情報監視タイムアウト GUID[" + GUID + "]");
            _healthTimer.Stop();
            Host.Abort();
        }

        // ロック用
        private static Object syncObj = new Object();
        // 接続イベント
        public delegate void JoinedEventHandler(string sender);
        //クライアントのコールバック
        IClientContractCallback callback = null;
        public string Message { get; set; }
        // GUID
        public Guid GUID { get; private set; }

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
        /// 接続
        /// </summary>
        /// <param name="name"></param>
        public void Join(Guid guid)
        {
            if( Host.State == CommunicationState.Opened )
            {
                return;
            }
            Console.WriteLine(guid);
            this.GUID = guid;
            callback = OperationContext.Current.GetCallbackChannel<IClientContractCallback>();
            OperationContext.Current.Channel.Closed += Channel_Closed;
            callback.SendData("test");
            CreateHealthTimer();
            App.Manager.Regist(this);

            DebugLog.LogInfo("::Join() 状態[" + Host.State.ToString() + "]");
            //_healthTimer.Start();
        }

        private void Channel_Closed(object sender, EventArgs e)
        {
            DebugLog.LogInfo("::Channel_Closed() GUID[" + GUID + "] 状態[" + Host.State.ToString() + "]");
        }

        /// <summary>
        /// 通知
        /// </summary>
        /// <param name="message"></param>
        public void Say(string message)
        {

        }

        public string GetData()
        {
            return "Hellow World";
        }

        public void Terminate()
        {
            if (GUID == null) 
            { 
                return; 
            }

            DebugLog.LogInfo("::Terminate() GUID[" + GUID + "] 状態[" + Host.State.ToString() + "]");
        }

        /// <summary>
        /// 
        /// </summary>
        public void Health()
        {
            Console.WriteLine("::Health() 状態[" + Host.State.ToString() + "]");

            if( ( Host.State == CommunicationState.Closed )
            ||  ( Host.State == CommunicationState.Closing)
            ||  ( Host.State == CommunicationState.Faulted) )
            {
                DebugLog.LogInfo("切断済み GUID[" + GUID + "]");
                return;
            }
            try
            {
                callback.Health();
                DebugLog.LogInfo("ヘルス情報送信 => GUID[" + GUID + "]");
            }
            catch(Exception ex)
            {
                DebugLog.LogInfo("ヘルス情報送信異常 => GUID[" + GUID + "] 状態[" +  Host.State.ToString() + "]");
            }
        }

        /// <summary>
        /// 
        /// </summary>
        public void Disconnect()
        {
            callback.Terminate();
        }
    }
 }
