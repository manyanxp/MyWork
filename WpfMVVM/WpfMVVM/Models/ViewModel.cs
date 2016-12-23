using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;

namespace WpfMVVM.Models
{
    #region ** Class : ViewModel
    /// <summary>
    /// ViewModel
    /// </summary>
    class ViewModel : ViewModelBase
    {
        // プロパティの値を保持するメンバ変数
        private int _property1 = 0;

        // プロパティ
        public int Property1
        {
            get { return _property1; }
            set
            {
                // 値が変更されたら、INotifyPropertyChanged.PropertyChanged を発生させる。
                if (_property1 != value)
                {
                    _property1 = value;
                    RaisePropertyChanged("Property1");

                    // 値は0以上、10以下。それ以外はエラー
                    if (value >= 0 && value <= 10)
                        ClearErrror("Property1");
                    else
                        SetError("Property1", "Error: argument out of range");
                }
            }
        }

        public ICommand Add1Command { get; private set; }

        // コンストラクタ
        public ViewModel()
        {
            Property1 = 0;
            Add1Command = CreateCommand(v => { Property1 = Property1 + 1; });
        }
    }
    #endregion
}
