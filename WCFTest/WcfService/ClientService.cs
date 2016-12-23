using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ServiceModel;

namespace WcfService
{
    /// <summary>
    /// サーバ -> クライアント通信用
    /// </summary>
    //[ServiceContract(Namespace = "WcfService", CallbackContract=typeof(IClientContractCallback))]
    [ServiceContract(Namespace = "http://WcfService")]
    public partial interface IClientContractCallback
    {
        /// <summary>
        /// セット／ゲット　メッセージ
        /// </summary>
        /// <param name="info"></param>
        /// <returns></returns>
        [OperationContract(IsOneWay = true)]
        void SendData(string message);

        [OperationContract(IsTerminating = true, IsOneWay = true)]
        void Terminate();
    }

    public partial interface IClientContractCallback
    {
        [OperationContract(IsOneWay = true)]
        void Health();
    }
}
