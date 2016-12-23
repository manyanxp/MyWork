using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ServiceModel;

namespace WcfService
{
    /// <summary>
    /// クライアント -> サーバ通信用
    /// </summary>
    //[ServiceContract(SessionMode = SessionMode.Required)]
    [ServiceContract(Namespace = "http://WcfService", SessionMode = SessionMode.Required, CallbackContract = typeof(IClientContractCallback))]
    public partial interface IServerContract
    {
        /// <summary>
        /// セット／ゲット　メッセージ
        /// </summary>
        /// <param name="info"></param>
        /// <returns></returns>
        [OperationContract(IsOneWay = true)]
        void SetMessage(string message);

        [OperationContract]
        string GetMessage();

        /// <summary>
        /// セッションを開始します。
        /// </summary>
        [OperationContract(IsInitiating = true, IsOneWay = true)]
        void Join(Guid guid);

        /// <summary>
        /// 通知
        /// </summary>
        /// <param name="message"></param>
        [OperationContract(IsOneWay = true)]
        void Say(string message);

        /// <summary>
        /// データを取得します。
        /// </summary>
        /// <returns>データ。</returns>
        [OperationContract(IsInitiating = false, IsTerminating = false)]
        string GetData();

        /// <summary>
        /// セッションを終了します。
        /// </summary>
        [OperationContract(IsInitiating = false, IsTerminating = true, IsOneWay=true)]
        void Terminate();
    }

    public partial interface IServerContract
    {
        /// <summary>
        /// ヘルス情報
        /// </summary>
        [OperationContract(IsInitiating = false, IsOneWay = true)]
        void Health();
    }
}
