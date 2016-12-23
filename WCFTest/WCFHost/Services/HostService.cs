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
 
    [ServiceBehavior(InstanceContextMode = InstanceContextMode.PerSession,
        ConcurrencyMode = ConcurrencyMode.Multiple)]
    public class HostService : IServerContract
    {
        public OperationContext Context { get { return (OperationContext)OperationContext.Current; } }

        public HostService()
        {
            if (this.Context == null)
            {
                Logger.DebugLog.LogError("OperationContextがNULLです.");
                return;
            }
            Logger.DebugLog.LogInfo("::HostService() ｲﾝｽﾀﾝｽ生成");
        }

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

            if (Context != null)
            {
                Context.Host.Abort();
            }
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
            if( Context == null )
            {
                return;
            }

            this.GUID = guid;

            DebugLog.LogInfo("::Join() GUID[" + GUID + "] 状態[" + Context.Host.State.ToString() + "]");
            
            callback = Context.GetCallbackChannel<IClientContractCallback>();
            Context.Channel.Closed += Channel_Closed;
            callback.SendData("test");
            CreateHealthTimer();

            Interpreter.ProtocolInterpreter.Instance.Regist(this);
            
            DebugLog.LogInfo("::Join() 登録完了 => GUID[" + GUID + "]");
            //_healthTimer.Start();
        }

        private void Channel_Closed(object sender, EventArgs e)
        {
            Interpreter.ProtocolInterpreter.Instance.Remove(this);
            DebugLog.LogInfo("::Channel_Closed() GUID[" + GUID + "]");
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
            if( Context == null )
            {
                return;
            }
            var host = (ServiceHostExtention)Context.Host;
            DebugLog.LogInfo("::Terminate() GUID[" + GUID + "] 状態[" + host.State.ToString() + "]");
        }

        /// <summary>
        /// 
        /// </summary>
        public void Health()
        {
            if (Context == null)
            {
                return;
            }
            var host = (ServiceHostExtention)Context.Host;

            Console.WriteLine("::Health() 状態[" + host.State.ToString() + "]");

            if ((host.State == CommunicationState.Closed)
            || (host.State == CommunicationState.Closing)
            || (host.State == CommunicationState.Faulted))
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
                DebugLog.LogInfo("ヘルス情報送信異常 => GUID[" + GUID + "] 状態[" +  host.State.ToString() + "]");
            }
        }

        /// <summary>
        /// 
        /// </summary>
        public void Disconnect()
        {
            if (Context == null)
            {
                return;
            }
            var host = (ServiceHostExtention)Context.Host;

            try
            {
                callback.Terminate();
            }
            catch (Exception ex)
            {
                DebugLog.LogInfo("切断異常 => GUID[" + GUID + "] 状態[" + host.State.ToString() + "]");
                DebugLog.LogInfo(ex.StackTrace);
            }
        }
    }
 }
