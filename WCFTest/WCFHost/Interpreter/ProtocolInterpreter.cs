using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.ServiceModel;
using WcfService;
using WCFHost;
using System.Timers;

using Cosmweb.Net.WCF;

namespace WCFHost.Interpreter
{
    public class ProtocolInterpreter : WcfHostBase<IServerContract>
    {
        #region Singleton
        private static ProtocolInterpreter single = new ProtocolInterpreter();
        private ProtocolInterpreter()
        {
            base.Create(typeof(Services.HostService),
                        "net.tcp://localhost:8080/ServerService",
                        base.DefaultMaxMessageSize);
        }
        public static ProtocolInterpreter Instance { get { return ProtocolInterpreter.single; } }
        #endregion

        /// <summary>
        /// ｻｰﾋﾞｽ管理用のﾃﾞｨｸｼｮﾅﾘ
        /// </summary>
        private static Object objSync = new Object();
        private Dictionary<Guid, Services.HostService> _services = 
            new Dictionary<Guid, Services.HostService>();
        protected Dictionary<Guid, Services.HostService> Services 
        { 
            get { return _services; }
            set { _services = value; } 
        }

        /// <summary>
        /// オープンイベント
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public override void _host_Opened(Object sender, EventArgs e)
        {
            Logger.DebugLog.LogInfo("Wcf Server オープン 状態[" + Host.State.ToString() + "]");

            // お試し
            Instance.Host.Tag = this;
        }

        /// <summary>
        /// クローズイベント
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public override void _host_Closed(object sender, EventArgs e)
        {
            base._host_Closed(sender, e);
            Logger.DebugLog.LogInfo("Wcf Server クローズ 状態[" + Host.State.ToString() + "]");
        }

        /// <summary>
        /// 異常イベント
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public override void _host_Faulted(Object sender, EventArgs e)
        {
            base._host_Faulted(sender, e);
            Logger.DebugLog.LogInfo("Wcf Server 異常? 状態[" + Host.State.ToString() + "]");
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public override void _host_UnknownMessageReceived(object sender, UnknownMessageReceivedEventArgs e)
        {
            Host.Abort();

            Logger.DebugLog.LogInfo("Wcf Server 不明な情報受信? 状態[" + Host.State.ToString() + "]");
        }

        /// <summary>
        /// ｻｰﾋﾞｽの登録
        /// </summary>
        /// <param name="hs"></param>
        public void Regist(Services.HostService hs)
        {
            lock (objSync)
            {
                if (Services.ContainsKey(hs.GUID))
                {

                    Logger.DebugLog.LogError("::Regist() GUIDが既に存在します。 GUID[" + hs.GUID + "]");
                    return;
                }
                else
                {
                    Services.Add(hs.GUID, hs);
                    Logger.DebugLog.LogInfo("::Regist() GUID[" + hs.GUID + "]");
                }
            }
        }

        /// <summary>
        /// ｻｰﾋﾞｽの削除
        /// </summary>
        /// <param name="hs"></param>
        public void Remove(Services.HostService hs)
        {
            lock (objSync)
            {
                if (Services.ContainsKey(hs.GUID))
                {
                    Services.Remove(hs.GUID);
                    Logger.DebugLog.LogInfo("::Remove() GUID[" + hs.GUID + "]");
                }
                else
                {
                    Logger.DebugLog.LogError("::Remove() GUIDが存在しません。 GUID[" + hs.GUID + "]");
                }
            }
        }

        /// <summary>
        /// クライアントの終了
        /// </summary>
        public void Terminate()
        {
            lock (objSync)
            {
                foreach (var interpreter in Services)
                {
                    interpreter.Value.Disconnect();
                }
            }
        }

        /// <summary>
        /// ヘルス情報
        /// </summary>
        public void Health()
        {
            lock (objSync)
            {
                foreach (var interpreter in Services)
                {
                    interpreter.Value.Health();
                }
            }
        }
    }
}
